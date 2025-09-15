from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json

from app.models.database import get_db
from app.models.schemas import User
from app.api.auth import get_current_user
from app.services.ai_orchestrator import AIOrchestrator

router = APIRouter()

# Global AI orchestrator instance (will be set from main.py)
ai_orchestrator: Optional[AIOrchestrator] = None

def set_ai_orchestrator(orchestrator: AIOrchestrator):
    """Set the AI orchestrator instance"""
    global ai_orchestrator
    ai_orchestrator = orchestrator

class VoiceQuery(BaseModel):
    language: str = "hi"

class TextQuery(BaseModel):
    query: str
    language: str = "hi"

class InsightRequest(BaseModel):
    insight_type: str = "all"  # all, inventory, customer, finance
    language: str = "hi"

@router.post("/voice")
async def process_voice_command(
    voice_data: VoiceQuery = Depends(),
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process voice command from user"""
    
    if not ai_orchestrator:
        raise HTTPException(status_code=500, detail="AI system not initialized")
    
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        # Process voice command
        result = await ai_orchestrator.process_voice_command(
            user_id=current_user.id,
            audio_data=audio_data,
            language=voice_data.language
        )
        
        return {
            "success": True,
            "result": result,
            "message": "Voice command processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process voice command: {str(e)}"
        )

@router.post("/text")
async def process_text_query(
    query_data: TextQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process text query from user"""
    
    if not ai_orchestrator:
        raise HTTPException(status_code=500, detail="AI system not initialized")
    
    try:
        # Process text query
        result = await ai_orchestrator.process_text_query(
            user_id=current_user.id,
            query=query_data.query,
            language=query_data.language
        )
        
        return {
            "success": True,
            "result": result,
            "message": "Text query processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process text query: {str(e)}"
        )

@router.get("/insights")
async def get_business_insights(
    insight_type: str = "all",
    language: str = "hi",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive business insights"""
    
    if not ai_orchestrator:
        raise HTTPException(status_code=500, detail="AI system not initialized")
    
    try:
        # Get business insights
        insights = await ai_orchestrator.get_business_insights(
            user_id=current_user.id,
            insight_type=insight_type,
            language=language
        )
        
        return {
            "success": True,
            "insights": insights,
            "message": "Business insights generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate insights: {str(e)}"
        )

@router.get("/status")
async def get_agent_status():
    """Get status of all AI agents"""
    
    if not ai_orchestrator:
        return {
            "status": "not_initialized",
            "agents": {},
            "message": "AI system is not initialized"
        }
    
    try:
        agent_status = {}
        for agent_name, agent in ai_orchestrator.agents.items():
            agent_status[agent_name] = {
                "name": agent.name,
                "expertise": agent.expertise,
                "status": "active"
            }
        
        return {
            "status": "operational",
            "agents": agent_status,
            "total_agents": len(ai_orchestrator.agents),
            "message": "All agents are operational"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "agents": {},
            "message": f"Error getting agent status: {str(e)}"
        }

@router.get("/capabilities")
async def get_system_capabilities():
    """Get system capabilities and features"""
    
    return {
        "multi_agent_system": {
            "inventory_agent": {
                "capabilities": [
                    "Stock level monitoring",
                    "Demand forecasting",
                    "Seasonal trend analysis",
                    "Festival demand prediction",
                    "Supplier recommendations",
                    "Expiry management"
                ]
            },
            "customer_agent": {
                "capabilities": [
                    "Customer segmentation",
                    "Personalized promotions",
                    "WhatsApp marketing automation",
                    "Loyalty program management",
                    "Customer behavior analysis",
                    "Retention strategies"
                ]
            },
            "finance_agent": {
                "capabilities": [
                    "Profitability analysis",
                    "Cash flow monitoring",
                    "Expense categorization",
                    "Revenue forecasting",
                    "Tax compliance insights",
                    "Credit score evaluation"
                ]
            }
        },
        "voice_interface": {
            "supported_languages": ["hi", "en", "te", "ta", "bn", "gu", "mr", "kn"],
            "features": [
                "Speech-to-text conversion",
                "Natural language understanding",
                "Text-to-speech response",
                "Multilingual support"
            ]
        },
        "integrations": {
            "marketplaces": ["ONDC", "Flipkart", "Amazon", "Meesho"],
            "payment_systems": ["UPI", "Razorpay"],
            "communication": ["WhatsApp Business", "SMS"]
        },
        "analytics": {
            "features": [
                "Real-time business insights",
                "Predictive analytics",
                "Seasonal forecasting",
                "Customer behavior analysis",
                "Financial health monitoring"
            ]
        }
    }

@router.post("/feedback")
async def submit_feedback(
    agent_type: str,
    interaction_id: str,
    rating: int,
    feedback: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit feedback for AI agent interactions"""
    
    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )
    
    # Log feedback for improvement
    # In production, store this in database for model training
    
    return {
        "success": True,
        "message": "Feedback submitted successfully",
        "data": {
            "agent_type": agent_type,
            "rating": rating,
            "feedback": feedback,
            "user_id": current_user.id
        }
    }

@router.get("/help")
async def get_help_information(
    language: str = "hi"
):
    """Get help information for using the AI system"""
    
    if language == "hi":
        help_info = {
            "voice_commands": [
                "आज की बिक्री बताओ",
                "स्टॉक की जांच करो",
                "ग्राहकों को मैसेज भेजो",
                "खर्च का हिसाब दो",
                "लाभ कितना है?"
            ],
            "features": [
                "आवाज़ से आदेश दें",
                "व्यापार की जानकारी पाएं",
                "स्वचालित प्रमोशन भेजें",
                "वित्तीय विश्लेषण प्राप्त करें"
            ],
            "tips": [
                "साफ़ आवाज़ में बोलें",
                "अपनी पसंदीदा भाषा चुनें",
                "नियमित रूप से डेटा अपडेट करें"
            ]
        }
    else:
        help_info = {
            "voice_commands": [
                "Tell me today's sales",
                "Check stock levels",
                "Send messages to customers",
                "Show expense analysis",
                "What is the profit?"
            ],
            "features": [
                "Voice commands",
                "Business insights",
                "Automated promotions",
                "Financial analysis"
            ],
            "tips": [
                "Speak clearly",
                "Choose your preferred language",
                "Update data regularly"
            ]
        }
    
    return {
        "help": help_info,
        "contact_support": "support@vyapaargpt.com",
        "documentation": "https://docs.vyapaargpt.com"
    }