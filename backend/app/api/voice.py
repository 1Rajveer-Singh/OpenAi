from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import openai
import os
import io
import base64

from app.models.database import get_db
from app.models.schemas import User
from app.api.auth import get_current_user

router = APIRouter()

class VoiceToTextRequest(BaseModel):
    language: str = "hi"

class TextToSpeechRequest(BaseModel):
    text: str
    language: str = "hi"
    voice: str = "alloy"

class LanguageDetectionRequest(BaseModel):
    text: str

@router.post("/speech-to-text")
async def convert_speech_to_text(
    language: str = "hi",
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Convert speech audio to text using OpenAI Whisper"""
    
    try:
        # Check if OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured"
            )
        
        # Read audio file
        audio_data = await audio_file.read()
        
        # Create a BytesIO object for the audio data
        audio_buffer = io.BytesIO(audio_data)
        audio_buffer.name = audio_file.filename or "audio.wav"
        
        # Initialize OpenAI client
        client = openai.OpenAI()
        
        # Transcribe audio using Whisper
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer,
            language=language if language != "hi" else None  # Whisper auto-detects Hindi better without explicit language
        )
        
        # Detect language if not provided
        detected_language = language
        if not language or language == "auto":
            # Simple language detection based on script
            text = transcript.text
            if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari script
                detected_language = "hi"
            elif any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu script
                detected_language = "te"
            elif any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil script
                detected_language = "ta"
            elif any('\u0980' <= char <= '\u09FF' for char in text):  # Bengali script
                detected_language = "bn"
            else:
                detected_language = "en"
        
        return {
            "success": True,
            "transcription": transcript.text,
            "language_detected": detected_language,
            "confidence": "high",  # Whisper doesn't provide confidence scores
            "audio_duration": None,  # Could be calculated if needed
            "message": "Speech converted to text successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Speech to text conversion failed: {str(e)}"
        )

@router.post("/text-to-speech")
async def convert_text_to_speech(
    request: TextToSpeechRequest,
    current_user: User = Depends(get_current_user)
):
    """Convert text to speech using OpenAI TTS"""
    
    try:
        # Check if OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured"
            )
        
        # Initialize OpenAI client
        client = openai.OpenAI()
        
        # Generate speech
        response = client.audio.speech.create(
            model="tts-1",
            voice=request.voice,
            input=request.text
        )
        
        # Convert audio to base64 for JSON response
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        
        return {
            "success": True,
            "audio_base64": audio_base64,
            "text": request.text,
            "language": request.language,
            "voice": request.voice,
            "message": "Text converted to speech successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text to speech conversion failed: {str(e)}"
        )

@router.post("/language-detect")
async def detect_language(
    request: LanguageDetectionRequest,
    current_user: User = Depends(get_current_user)
):
    """Detect language of given text"""
    
    try:
        text = request.text
        
        # Simple script-based language detection
        detected_languages = []
        
        # Check for different Indian scripts
        if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari (Hindi)
            detected_languages.append({"language": "hi", "name": "Hindi", "confidence": 0.9})
        
        if any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu
            detected_languages.append({"language": "te", "name": "Telugu", "confidence": 0.9})
        
        if any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil
            detected_languages.append({"language": "ta", "name": "Tamil", "confidence": 0.9})
        
        if any('\u0980' <= char <= '\u09FF' for char in text):  # Bengali
            detected_languages.append({"language": "bn", "name": "Bengali", "confidence": 0.9})
        
        if any('\u0A80' <= char <= '\u0AFF' for char in text):  # Gujarati
            detected_languages.append({"language": "gu", "name": "Gujarati", "confidence": 0.9})
        
        if any('\u0900' <= char <= '\u094F' for char in text):  # Marathi (shares Devanagari)
            detected_languages.append({"language": "mr", "name": "Marathi", "confidence": 0.7})
        
        if any('\u0C80' <= char <= '\u0CFF' for char in text):  # Kannada
            detected_languages.append({"language": "kn", "name": "Kannada", "confidence": 0.9})
        
        # If no Indian scripts detected, assume English
        if not detected_languages:
            detected_languages.append({"language": "en", "name": "English", "confidence": 0.8})
        
        # Primary detection
        primary_language = detected_languages[0] if detected_languages else {"language": "en", "name": "English", "confidence": 0.5}
        
        return {
            "success": True,
            "primary_language": primary_language,
            "all_detected": detected_languages,
            "text": text,
            "message": "Language detected successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Language detection failed: {str(e)}"
        )

@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages"""
    
    return {
        "supported_languages": [
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी", "script": "Devanagari"},
            {"code": "en", "name": "English", "native_name": "English", "script": "Latin"},
            {"code": "te", "name": "Telugu", "native_name": "తెలుగు", "script": "Telugu"},
            {"code": "ta", "name": "Tamil", "native_name": "தமிழ்", "script": "Tamil"},
            {"code": "bn", "name": "Bengali", "native_name": "বাংলা", "script": "Bengali"},
            {"code": "gu", "name": "Gujarati", "native_name": "ગુજરાતી", "script": "Gujarati"},
            {"code": "mr", "name": "Marathi", "native_name": "मराठी", "script": "Devanagari"},
            {"code": "kn", "name": "Kannada", "native_name": "ಕನ್ನಡ", "script": "Kannada"}
        ],
        "default_language": "hi",
        "voice_support": {
            "text_to_speech": ["hi", "en"],
            "speech_to_text": ["hi", "en", "te", "ta", "bn", "gu", "mr", "kn"]
        },
        "message": "These languages are supported by VyapaarGPT"
    }

@router.get("/voice-settings")
async def get_voice_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's voice settings and preferences"""
    
    return {
        "user_preferences": {
            "preferred_language": current_user.preferred_language,
            "voice_commands_enabled": True,
            "auto_language_detection": True,
            "voice_feedback_enabled": True
        },
        "available_voices": [
            {"id": "alloy", "name": "Alloy", "description": "Neutral, balanced voice"},
            {"id": "echo", "name": "Echo", "description": "Clear, professional voice"},
            {"id": "fable", "name": "Fable", "description": "Warm, storytelling voice"},
            {"id": "onyx", "name": "Onyx", "description": "Deep, authoritative voice"},
            {"id": "nova", "name": "Nova", "description": "Bright, energetic voice"},
            {"id": "shimmer", "name": "Shimmer", "description": "Soft, gentle voice"}
        ],
        "recommended_voice": "alloy",
        "voice_quality_settings": {
            "speed": "normal",
            "pitch": "normal",
            "volume": "normal"
        }
    }

@router.put("/voice-settings")
async def update_voice_settings(
    preferred_language: Optional[str] = None,
    voice_commands_enabled: Optional[bool] = None,
    auto_language_detection: Optional[bool] = None,
    voice_feedback_enabled: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's voice settings"""
    
    # Update user's preferred language if provided
    if preferred_language:
        supported_languages = ["hi", "en", "te", "ta", "bn", "gu", "mr", "kn"]
        if preferred_language not in supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Language '{preferred_language}' not supported. Supported languages: {supported_languages}"
            )
        current_user.preferred_language = preferred_language
        db.commit()
    
    return {
        "message": "Voice settings updated successfully",
        "updated_settings": {
            "preferred_language": current_user.preferred_language,
            "voice_commands_enabled": voice_commands_enabled,
            "auto_language_detection": auto_language_detection,
            "voice_feedback_enabled": voice_feedback_enabled
        }
    }

@router.post("/test-voice")
async def test_voice_functionality(
    test_type: str = "greeting",  # greeting, sample_command, echo
    language: str = None,
    current_user: User = Depends(get_current_user)
):
    """Test voice functionality with sample phrases"""
    
    # Use user's preferred language if not specified
    if not language:
        language = current_user.preferred_language
    
    # Sample test phrases in different languages
    test_phrases = {
        "greeting": {
            "hi": "नमस्ते! मैं आपका AI व्यापार साथी हूं। आप मुझसे अपने व्यापार के बारे में पूछ सकते हैं।",
            "en": "Hello! I'm your AI business partner. You can ask me about your business.",
            "te": "నమస్కారం! నేను మీ AI వ్యాపార భాగస్వామిని. మీరు మీ వ్యాపారం గురించి నన్ను అడగవచ్చు.",
            "ta": "வணக்கம்! நான் உங்கள் AI வணிக பங்குதாரர். உங்கள் வணிகத்தைப் பற்றி என்னிடம் கேட்கலாம்.",
            "bn": "নমস্কার! আমি আপনার AI ব্যবসায়িক সহযোগী। আপনি আপনার ব্যবসা সম্পর্কে আমাকে জিজ্ঞাসা করতে পারেন।"
        },
        "sample_command": {
            "hi": "आज की बिक्री कितनी है? स्टॉक कम है कौन सा? ग्राहकों को मैसेज भेजो।",
            "en": "What are today's sales? Which stock is low? Send message to customers.",
            "te": "ఈరోజు అమ్మకాలు ఎంత? ఏ స్టాక్ తక్కువ ఉంది? కస్టమర్లకు మెసేజ్ పంపండి.",
            "ta": "இன்றைய விற்பனை எவ்வளவு? எந்த பொருள் குறைவாக உள்ளது? வாடிக்கையாளர்களுக்கு செய்தி அனுப்பு.",
            "bn": "আজকের বিক্রয় কত? কোন স্টক কম আছে? গ্রাহকদের বার্তা পাঠান।"
        }
    }
    
    # Get test phrase
    phrase = test_phrases.get(test_type, {}).get(language, test_phrases["greeting"]["en"])
    
    try:
        # Generate audio for the test phrase
        client = openai.OpenAI()
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=phrase
        )
        
        # Convert to base64
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        
        return {
            "success": True,
            "test_type": test_type,
            "language": language,
            "text": phrase,
            "audio_base64": audio_base64,
            "message": "Voice test completed successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "test_type": test_type,
            "language": language,
            "text": phrase,
            "error": str(e),
            "message": "Voice test failed, but text is provided"
        }