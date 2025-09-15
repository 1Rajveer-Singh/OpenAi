import asyncio
from typing import Dict, Any, List, Optional
from loguru import logger
import openai
import os
from datetime import datetime

from app.agents.inventory_agent import InventoryAgent
from app.agents.customer_agent import CustomerAgent
from app.agents.finance_agent import FinanceAgent

class AIOrchestrator:
    """
    Central orchestrator for the multi-agent AI system in VyapaarGPT.
    Coordinates between Inventory, Customer, and Finance agents.
    """
    
    def __init__(self):
        self.openai_client = None
        self.agents = {}
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize all AI agents and OpenAI client"""
        try:
            # Initialize OpenAI client
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.openai_client = openai.AsyncOpenAI()
            
            # Initialize agents
            self.agents = {
                "inventory": InventoryAgent(self.openai_client),
                "customer": CustomerAgent(self.openai_client),
                "finance": FinanceAgent(self.openai_client)
            }
            
            # Initialize each agent
            for agent_name, agent in self.agents.items():
                await agent.initialize()
                logger.info(f"✅ {agent_name.title()} Agent initialized")
            
            self.is_initialized = True
            logger.info("🎯 AI Orchestrator fully initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI Orchestrator: {e}")
            raise e
    
    async def process_voice_command(
        self, 
        user_id: int, 
        audio_data: bytes, 
        language: str = "hi"
    ) -> Dict[str, Any]:
        """
        Process voice command from user and route to appropriate agent
        """
        try:
            # Transcribe audio using Whisper
            transcription = await self._transcribe_audio(audio_data, language)
            
            # Analyze intent and route to appropriate agent
            intent_analysis = await self._analyze_intent(transcription, language)
            
            # Route to appropriate agent
            response = await self._route_to_agent(
                user_id, 
                transcription, 
                intent_analysis, 
                language
            )
            
            # Generate voice response
            audio_response = await self._generate_voice_response(
                response["text"], 
                language
            )
            
            return {
                "transcription": transcription,
                "intent": intent_analysis,
                "response": response,
                "audio_response": audio_response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            return {
                "error": "Voice processing failed",
                "message": "कृपया फिर से कोशिश करें" if language == "hi" else "Please try again"
            }
    
    async def process_text_query(
        self, 
        user_id: int, 
        query: str, 
        language: str = "hi"
    ) -> Dict[str, Any]:
        """
        Process text query from user
        """
        try:
            # Analyze intent
            intent_analysis = await self._analyze_intent(query, language)
            
            # Route to appropriate agent
            response = await self._route_to_agent(
                user_id, 
                query, 
                intent_analysis, 
                language
            )
            
            return {
                "query": query,
                "intent": intent_analysis,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing text query: {e}")
            return {
                "error": "Query processing failed",
                "message": "कुछ गलत हुआ है, कृपया फिर से कोशिश करें" if language == "hi" else "Something went wrong, please try again"
            }
    
    async def get_business_insights(
        self, 
        user_id: int, 
        insight_type: str = "all",
        language: str = "hi"
    ) -> Dict[str, Any]:
        """
        Get comprehensive business insights from all agents
        """
        try:
            insights = {}
            
            if insight_type in ["all", "inventory"]:
                insights["inventory"] = await self.agents["inventory"].get_insights(user_id)
            
            if insight_type in ["all", "customer"]:
                insights["customer"] = await self.agents["customer"].get_insights(user_id)
            
            if insight_type in ["all", "finance"]:
                insights["finance"] = await self.agents["finance"].get_insights(user_id)
            
            # Generate summary using GPT
            summary = await self._generate_insights_summary(insights, language)
            
            return {
                "insights": insights,
                "summary": summary,
                "recommendations": await self._generate_recommendations(insights, language),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting business insights: {e}")
            return {"error": "Failed to generate insights"}
    
    async def _transcribe_audio(self, audio_data: bytes, language: str) -> str:
        """Transcribe audio using OpenAI Whisper"""
        try:
            # Convert audio data to file-like object
            # This is a simplified version - in production, handle audio formats properly
            response = await self.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_data,
                language=language if language != "hi" else "hi"
            )
            return response.text
        except Exception as e:
            logger.error(f"Audio transcription failed: {e}")
            return ""
    
    async def _analyze_intent(self, text: str, language: str) -> Dict[str, Any]:
        """Analyze user intent using GPT-4"""
        try:
            prompt = f"""
            Analyze the following business query in {language} and classify the intent:
            
            Query: "{text}"
            
            Classify into one of these categories with confidence score:
            1. INVENTORY - stock checking, demand forecasting, supplier management
            2. CUSTOMER - customer engagement, promotions, loyalty programs
            3. FINANCE - sales analysis, profit margins, expense tracking
            4. GENERAL - greetings, general business questions
            
            Respond in JSON format:
            {{
                "primary_intent": "category",
                "confidence": 0.0-1.0,
                "entities": ["extracted entities"],
                "language": "{language}",
                "urgent": true/false
            }}
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            # Parse JSON response
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Intent analysis failed: {e}")
            return {
                "primary_intent": "GENERAL",
                "confidence": 0.5,
                "entities": [],
                "language": language,
                "urgent": False
            }
    
    async def _route_to_agent(
        self, 
        user_id: int, 
        query: str, 
        intent: Dict[str, Any], 
        language: str
    ) -> Dict[str, Any]:
        """Route query to appropriate agent based on intent"""
        try:
            agent_mapping = {
                "INVENTORY": "inventory",
                "CUSTOMER": "customer", 
                "FINANCE": "finance"
            }
            
            primary_intent = intent.get("primary_intent", "GENERAL")
            
            if primary_intent in agent_mapping:
                agent = self.agents[agent_mapping[primary_intent]]
                return await agent.process_query(user_id, query, intent, language)
            else:
                # Handle general queries
                return await self._handle_general_query(query, language)
                
        except Exception as e:
            logger.error(f"Agent routing failed: {e}")
            return {
                "text": "मुझे समझने में कठिनाई हो रही है" if language == "hi" else "I'm having trouble understanding",
                "agent": "none",
                "success": False
            }
    
    async def _handle_general_query(self, query: str, language: str) -> Dict[str, Any]:
        """Handle general business queries"""
        return {
            "text": "नमस्ते! मैं आपका AI व्यापार साथी हूं। आप मुझसे स्टॉक, ग्राहक या बिक्री के बारे में पूछ सकते हैं।" if language == "hi" 
                   else "Hello! I'm your AI business partner. You can ask me about stock, customers, or sales.",
            "agent": "general",
            "success": True
        }
    
    async def _generate_voice_response(self, text: str, language: str) -> bytes:
        """Generate voice response using OpenAI TTS"""
        try:
            response = await self.openai_client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            return response.content
        except Exception as e:
            logger.error(f"Voice generation failed: {e}")
            return b""
    
    async def _generate_insights_summary(self, insights: Dict[str, Any], language: str) -> str:
        """Generate a summary of business insights"""
        try:
            prompt = f"""
            Create a business summary in {language} based on these insights:
            {insights}
            
            Provide a concise, actionable summary for a small business owner.
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return "व्यापार की जानकारी उपलब्ध नहीं है" if language == "hi" else "Business information not available"
    
    async def _generate_recommendations(self, insights: Dict[str, Any], language: str) -> List[str]:
        """Generate actionable business recommendations"""
        try:
            prompt = f"""
            Based on these business insights, provide 3-5 actionable recommendations in {language}:
            {insights}
            
            Focus on practical steps the business owner can take immediately.
            Return as a JSON array of strings.
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Recommendations generation failed: {e}")
            return ["व्यापार में सुधार के लिए डेटा का विश्लेषण करें" if language == "hi" else "Analyze data for business improvement"]
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            for agent in self.agents.values():
                if hasattr(agent, 'cleanup'):
                    await agent.cleanup()
            logger.info("🧹 AI Orchestrator cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")