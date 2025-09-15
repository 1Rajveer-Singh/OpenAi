"""
VyapaarGPT - AI-Powered Business OS for India's Local Shops & Startups
Demo Version
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="VyapaarGPT API - Demo",
    description="AI-Powered Business OS for India's Local Shops & Startups",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("🚀 VyapaarGPT Demo Backend Starting Up...")
    logger.info("🇮🇳 AI Business OS for India's MSMEs")

@app.on_event("shutdown") 
async def shutdown_event():
    """Shutdown event"""
    logger.info("🛑 VyapaarGPT Demo Backend Shutting Down...")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system status"""
    return {
        "message": "🇮🇳 VyapaarGPT - AI Business OS for India",
        "status": "running",
        "version": "1.0.0",
        "mode": "demo",
        "features": {
            "voice_interface": "8+ Indian Languages (Hindi, Telugu, Tamil, Bengali, Gujarati, Marathi, Kannada, English)",
            "ai_agents": "Inventory, Customer, Finance Management",
            "integrations": "WhatsApp, UPI, ONDC, Marketplaces",
            "security": "AES-256 Encryption & Indian Data Compliance"
        },
        "tech_stack": {
            "backend": "FastAPI + Python",
            "database": "PostgreSQL with SQLAlchemy",
            "ai": "OpenAI GPT-4o + Whisper",
            "frontend": "React Native + Expo"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "VyapaarGPT Demo Backend",
        "uptime": "running",
        "timestamp": "2024-01-15T10:30:00Z"
    }

# Demo AI Agents endpoint
@app.get("/api/agents")
async def get_agents():
    """Get AI agents information"""
    return {
        "agents": {
            "inventory_agent": {
                "name": "Inventory Management AI",
                "description": "स्मार्ट स्टॉक ट्रैकिंग और अलर्ट (Smart stock tracking and alerts)",
                "capabilities": [
                    "Stock level monitoring",
                    "Low stock alerts", 
                    "Demand prediction",
                    "Supplier recommendations",
                    "Price optimization"
                ],
                "languages": ["Hindi", "English", "Telugu", "Tamil"]
            },
            "customer_agent": {
                "name": "Customer Engagement AI",
                "description": "ग्राहक व्यवहार विश्लेषण (Customer behavior analysis)",
                "capabilities": [
                    "Customer behavior analysis",
                    "Personalized recommendations",
                    "Automated follow-ups",
                    "Loyalty program management",
                    "WhatsApp integration"
                ],
                "languages": ["Hindi", "English", "Bengali", "Gujarati"]
            },
            "finance_agent": {
                "name": "Financial Analytics AI", 
                "description": "वित्तीय विश्लेषण और रिपोर्ट (Financial analysis and reports)",
                "capabilities": [
                    "Cash flow analysis",
                    "Expense tracking",
                    "Tax calculations",
                    "Financial insights",
                    "UPI integration"
                ],
                "languages": ["Hindi", "English", "Marathi", "Kannada"]
            }
        }
    }

# Demo Voice Interface endpoint
@app.get("/api/voice")
async def voice_interface():
    """Voice interface demo"""
    return {
        "voice_interface": {
            "status": "active",
            "supported_languages": [
                {"code": "hi", "name": "हिन्दी (Hindi)", "native": "हिन्दी"},
                {"code": "te", "name": "తెలుగు (Telugu)", "native": "తెలుగు"},
                {"code": "ta", "name": "தமிழ் (Tamil)", "native": "தமிழ்"},
                {"code": "bn", "name": "বাংলা (Bengali)", "native": "বাংলা"},
                {"code": "gu", "name": "ગુજરાતી (Gujarati)", "native": "ગુજરાતી"},
                {"code": "mr", "name": "मराठी (Marathi)", "native": "मराठी"},
                {"code": "kn", "name": "ಕನ್ನಡ (Kannada)", "native": "ಕನ್ನಡ"},
                {"code": "en", "name": "English", "native": "English"}
            ],
            "sample_commands": {
                "hindi": [
                    "नया उत्पाद जोड़ें",
                    "आज की बिक्री दिखाएं",
                    "स्टॉक चेक करें",
                    "नया ग्राहक जोड़ें"
                ],
                "english": [
                    "Add new product",
                    "Show today's sales",
                    "Check inventory",
                    "Add new customer"
                ],
                "telugu": [
                    "కొత్త ఉత్పత్తిని జోడించండి",
                    "నేటి అమ్మకాలను చూపించండి"
                ]
            }
        }
    }

# Demo Dashboard endpoint
@app.get("/api/dashboard")
async def dashboard():
    """Demo dashboard data"""
    return {
        "business_overview": {
            "business_name": "राम इलेक्ट्रॉनिक्स (Ram Electronics)",
            "owner": "राम शर्मा (Ram Sharma)",
            "location": "दिल्ली, भारत (Delhi, India)",
            "business_type": "Electronics Retail"
        },
        "today_stats": {
            "sales": {"amount": 15750.50, "currency": "INR", "orders": 23},
            "customers": {"total": 234, "new_today": 3},
            "inventory": {"total_items": 1250, "low_stock_alerts": 5}
        },
        "weekly_performance": {
            "sales_trend": [12500, 14200, 13800, 15300, 16100, 14700, 15750],
            "customer_growth": [220, 225, 228, 231, 234, 234, 237],
            "top_selling_categories": [
                {"name": "Smartphones", "sales": 8500},
                {"name": "Accessories", "sales": 3200},
                {"name": "Audio", "sales": 2800},
                {"name": "Storage", "sales": 1250}
            ]
        },
        "recent_activities": [
            {
                "time": "5 minutes ago",
                "activity": "New order from सुनीता देवी (Sunita Devi)",
                "amount": 2499.00,
                "type": "sale"
            },
            {
                "time": "15 minutes ago", 
                "activity": "Stock alert: iPhone chargers running low",
                "count": 3,
                "type": "alert"
            },
            {
                "time": "30 minutes ago",
                "activity": "UPI payment received from राज कुमार (Raj Kumar)",
                "amount": 1850.00,
                "type": "payment"
            }
        ]
    }

# Demo Marketplace Integration endpoint
@app.get("/api/marketplace")
async def marketplace_integrations():
    """Demo marketplace integrations"""
    return {
        "integrations": {
            "ondc": {
                "name": "Open Network for Digital Commerce",
                "status": "connected",
                "description": "भारत सरकार का डिजिटल कॉमर्स नेटवर्क",
                "products_listed": 45,
                "orders_received": 12
            },
            "flipkart": {
                "name": "Flipkart Seller Hub",
                "status": "connected", 
                "description": "भारत का सबसे बड़ा ई-कॉमर्स प्लेटफॉर्म",
                "products_listed": 38,
                "orders_received": 8
            },
            "amazon": {
                "name": "Amazon India Seller",
                "status": "connected",
                "description": "Amazon India marketplace integration",
                "products_listed": 42,
                "orders_received": 15
            },
            "meesho": {
                "name": "Meesho Supplier Panel",
                "status": "connected",
                "description": "Social commerce platform",
                "products_listed": 28,
                "orders_received": 6
            }
        },
        "sync_status": {
            "last_sync": "2024-01-15T09:30:00Z",
            "next_sync": "2024-01-15T10:30:00Z",
            "status": "healthy"
        }
    }

# Demo Payment Integration endpoint  
@app.get("/api/payments")
async def payment_integrations():
    """Demo payment integrations"""
    return {
        "payment_methods": {
            "upi": {
                "name": "Unified Payment Interface",
                "status": "active",
                "providers": ["PhonePe", "GPay", "Paytm", "BHIM"],
                "today_transactions": 18,
                "total_amount": 12350.50
            },
            "razorpay": {
                "name": "Razorpay Payment Gateway", 
                "status": "active",
                "supported": ["Cards", "Net Banking", "Wallets"],
                "today_transactions": 5,
                "total_amount": 3400.00
            },
            "cash": {
                "name": "Cash Payments",
                "status": "active", 
                "today_transactions": 8,
                "total_amount": 2850.00
            }
        },
        "transaction_summary": {
            "total_today": 31,
            "total_amount": 18600.50,
            "currency": "INR",
            "average_transaction": 600.02
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Starting VyapaarGPT Demo on {host}:{port}")
    
    uvicorn.run(
        "demo_main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )