from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from loguru import logger

from app.api import auth, agents, inventory, customers, finance, voice, marketplace
from app.models.database import engine, Base
from app.services.ai_orchestrator import AIOrchestrator

# Load environment variables
load_dotenv()

# Initialize AI Orchestrator
ai_orchestrator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global ai_orchestrator
    
    # Startup
    logger.info("🚀 Starting VyapaarGPT AI Business OS")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("📊 Database tables created")
    
    # Initialize AI Orchestrator
    ai_orchestrator = AIOrchestrator()
    await ai_orchestrator.initialize()
    logger.info("🤖 AI Multi-Agent system initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down VyapaarGPT")
    if ai_orchestrator:
        await ai_orchestrator.cleanup()

# Create FastAPI app
app = FastAPI(
    title="VyapaarGPT API",
    description="AI-Powered Business OS for India's Local Shops & Startups",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(agents.router, prefix="/api/agents", tags=["AI Agents"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory Management"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customer Management"])
app.include_router(finance.router, prefix="/api/finance", tags=["Financial Analytics"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice Interface"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace Integration"])

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "🎯 VyapaarGPT API - Your AI Business Partner",
        "version": "1.0.0",
        "description": "AI-Powered Business OS for India's Local Shops & Startups",
        "tagline": "Speak, and your business runs smarter",
        "features": [
            "🤖 Multi-Agent AI System",
            "🗣️ Voice-First Interface",
            "📊 Smart Inventory Management",
            "💰 Financial Health Insights",
            "🛒 Marketplace Integration",
            "🌍 Multilingual Support"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_system": "operational" if ai_orchestrator else "initializing",
        "database": "connected",
        "version": "1.0.0"
    }

@app.get("/api/stats")
async def get_api_stats():
    """Get API usage statistics"""
    return {
        "total_agents": 3,
        "active_users": 0,  # Implement user tracking
        "supported_languages": ["hi", "en", "te", "ta", "bn", "gu", "mr", "kn"],
        "marketplace_integrations": ["ONDC", "Flipkart", "Amazon", "Meesho"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )