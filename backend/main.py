from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="VyapaarGPT API",
    description="AI-Powered Business OS for India 🇮🇳",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
@app.get("/api")
async def root():
    return {
        "message": "🇮🇳 VyapaarGPT API - AI Business OS for India",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "AI Agents for Business Automation",
            "Voice Interface (8+ Indian Languages)",
            "Marketplace Integrations",
            "Real-time Analytics",
            "Customer Management",
            "Inventory Optimization"
        ]
    }

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "VyapaarGPT API",
        "timestamp": datetime.now().isoformat()
    }

# Dashboard endpoint
@app.get("/api/dashboard")
async def get_dashboard():
    return {
        "business_name": "Sharma General Store",
        "owner": "राजेश शर्मा",
        "stats": {
            "today_revenue": "₹75,450",
            "total_orders": 342,
            "active_customers": 2847,
            "customer_satisfaction": "94%"
        },
        "sales_data": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
            "values": [25000, 32000, 28000, 45000, 52000, 48000, 65000]
        },
        "category_data": {
            "labels": ["Groceries", "Electronics", "Clothing", "Books", "Others"],
            "values": [35, 25, 20, 15, 5]
        },
        "recent_activities": [
            {
                "type": "order",
                "title": "New Order Received",
                "description": "Order #ORD-2024-156 from Priya Sharma",
                "amount": "₹2,350",
                "time": "2 minutes ago",
                "icon": "shopping-bag"
            },
            {
                "type": "customer",
                "title": "New Customer Registration",
                "description": "Amit Kumar joined as a new customer",
                "time": "15 minutes ago",
                "icon": "user-plus"
            },
            {
                "type": "alert",
                "title": "Low Stock Alert",
                "description": "Basmati Rice - Only 5 units remaining",
                "time": "1 hour ago",
                "icon": "exclamation-triangle"
            }
        ]
    }

# AI Agents endpoint
@app.get("/api/agents")
async def get_ai_agents():
    return {
        "agents": [
            {
                "id": "inventory_agent",
                "name": "Inventory Manager",
                "description": "Manages stock levels, reorder points, and inventory optimization",
                "status": "active",
                "tasks_today": 23,
                "accuracy": "98%",
                "capabilities": [
                    "Stock level monitoring",
                    "Automatic reorder suggestions",
                    "Demand forecasting",
                    "Supplier management"
                ]
            },
            {
                "id": "customer_agent",
                "name": "Customer Support",
                "description": "Handles customer queries and provides instant responses",
                "status": "active",
                "tasks_today": 156,
                "accuracy": "96%",
                "capabilities": [
                    "24/7 customer support",
                    "Multi-language assistance",
                    "Order tracking",
                    "Complaint resolution"
                ]
            },
            {
                "id": "finance_agent",
                "name": "Finance Assistant",
                "description": "Tracks expenses, generates reports, and manages invoices",
                "status": "active",
                "tasks_today": 89,
                "accuracy": "99%",
                "capabilities": [
                    "Expense tracking",
                    "Invoice generation",
                    "Financial reporting",
                    "Tax calculations"
                ]
            }
        ]
    }

# Voice interface endpoint
@app.get("/api/voice")
async def get_voice_interface():
    return {
        "supported_languages": [
            {"code": "hi", "name": "हिंदी", "native": "Hindi"},
            {"code": "en", "name": "English", "native": "English"},
            {"code": "te", "name": "తెలుగు", "native": "Telugu"},
            {"code": "ta", "name": "தமிழ்", "native": "Tamil"},
            {"code": "bn", "name": "বাংলা", "native": "Bengali"},
            {"code": "gu", "name": "ગુજરાતી", "native": "Gujarati"},
            {"code": "kn", "name": "ಕನ್ನಡ", "native": "Kannada"},
            {"code": "ml", "name": "മലയാളം", "native": "Malayalam"}
        ],
        "sample_commands": {
            "hindi": [
                "नया उत्पाद जोड़ें",
                "आज की बिक्री दिखाएं", 
                "स्टॉक चेक करें",
                "ग्राहक सूची दिखाएं"
            ],
            "english": [
                "Add new product",
                "Show today's sales",
                "Check inventory",
                "Display customer list"
            ]
        },
        "features": [
            "Natural language processing",
            "Context-aware responses",
            "Multi-turn conversations",
            "Business domain expertise"
        ]
    }

# Marketplace integrations
@app.get("/api/marketplace")
async def get_marketplace_integrations():
    return {
        "integrations": [
            {
                "name": "ONDC Network",
                "status": "connected",
                "orders_today": 45,
                "revenue_today": "₹25,000",
                "sync_status": "active",
                "last_sync": "2 minutes ago"
            },
            {
                "name": "Flipkart",
                "status": "connected",
                "orders_today": 23,
                "revenue_today": "₹18,500",
                "sync_status": "active",
                "last_sync": "5 minutes ago"
            },
            {
                "name": "Amazon",
                "status": "pending",
                "orders_today": 0,
                "revenue_today": "₹0",
                "sync_status": "setup_required",
                "last_sync": "never"
            },
            {
                "name": "Meesho",
                "status": "connected",
                "orders_today": 12,
                "revenue_today": "₹8,200",
                "sync_status": "active",
                "last_sync": "1 minute ago"
            }
        ],
        "total_orders": 80,
        "total_revenue": "₹51,700",
        "sync_frequency": "real-time"
    }

# Inventory endpoint
@app.get("/api/inventory")
async def get_inventory():
    return {
        "summary": {
            "total_products": 1234,
            "low_stock_alerts": 23,
            "inventory_value": "₹2,10,000",
            "stock_turnover": "89%"
        },
        "products": [
            {
                "id": "PROD-001",
                "name": "Basmati Rice Premium",
                "category": "Groceries",
                "stock": 45,
                "price": 180,
                "status": "in_stock",
                "supplier": "Local Farmer Cooperative"
            },
            {
                "id": "PROD-002", 
                "name": "Samsung Galaxy Earbuds",
                "category": "Electronics",
                "stock": 8,
                "price": 12999,
                "status": "low_stock",
                "supplier": "Samsung India"
            },
            {
                "id": "PROD-003",
                "name": "Cotton Kurta Set",
                "category": "Clothing", 
                "stock": 23,
                "price": 899,
                "status": "in_stock",
                "supplier": "Textile Manufacturer"
            }
        ]
    }

# Customers endpoint
@app.get("/api/customers")
async def get_customers():
    return {
        "summary": {
            "total_customers": 2567,
            "active_customers": 834,
            "avg_order_value": "₹1,250",
            "customer_retention": "92%"
        },
        "customers": [
            {
                "id": "CUST-001",
                "name": "Priya Sharma",
                "phone": "+91 9876543210",
                "email": "priya@email.com",
                "orders": 15,
                "total_spent": 18500,
                "last_order": "2024-09-13",
                "status": "active"
            },
            {
                "id": "CUST-002",
                "name": "Rajesh Kumar", 
                "phone": "+91 9876543211",
                "email": "rajesh@email.com",
                "orders": 8,
                "total_spent": 12300,
                "last_order": "2024-09-08",
                "status": "active"
            }
        ]
    }

# Analytics endpoint
@app.get("/api/analytics")
async def get_analytics():
    return {
        "revenue_analytics": {
            "daily": [1500, 2300, 1800, 2800, 3200, 2900, 3500],
            "weekly": [15000, 18000, 16500, 21000, 19500, 23000, 25000],
            "monthly": [85000, 92000, 88000, 105000, 98000, 112000, 120000]
        },
        "customer_growth": {
            "new_customers": [12, 18, 15, 22, 19, 25, 28],
            "returning_customers": [45, 52, 48, 58, 55, 62, 67]
        },
        "top_products": [
            {"name": "Basmati Rice", "sales": 145, "revenue": "₹26,100"},
            {"name": "Smartphone", "sales": 23, "revenue": "₹2,99,000"},
            {"name": "Cotton Kurta", "sales": 67, "revenue": "₹60,233"}
        ],
        "insights": [
            "Sales increased by 15% this week",
            "Electronics category showing strong growth",
            "Customer retention improved by 3%",
            "Inventory turnover is optimal"
        ]
    }

# Settings endpoint
@app.get("/api/settings")
async def get_settings():
    return {
        "business_profile": {
            "name": "Sharma General Store",
            "owner": "राजेश शर्मा", 
            "gst_number": "07AAACH7409R1ZX",
            "address": "Main Market, Delhi",
            "phone": "+91 9876543210",
            "email": "sharma.store@email.com"
        },
        "preferences": {
            "language": "hi",
            "currency": "INR",
            "timezone": "Asia/Kolkata",
            "theme": "light"
        },
        "integrations": {
            "payment_gateways": ["UPI", "Paytm", "PhonePe", "GPay"],
            "sms_service": "enabled",
            "whatsapp_business": "connected",
            "email_notifications": "enabled"
        }
    }

# Payment systems endpoint
@app.get("/api/payments")
async def get_payment_systems():
    return {
        "supported_methods": [
            {
                "name": "UPI",
                "status": "active",
                "daily_transactions": 156,
                "daily_amount": "₹45,600"
            },
            {
                "name": "PhonePe",
                "status": "active", 
                "daily_transactions": 89,
                "daily_amount": "₹23,400"
            },
            {
                "name": "Google Pay",
                "status": "active",
                "daily_transactions": 67,
                "daily_amount": "₹18,900"
            },
            {
                "name": "Paytm",
                "status": "active",
                "daily_transactions": 34,
                "daily_amount": "₹12,100"
            }
        ],
        "total_transactions": 346,
        "total_amount": "₹1,00,000",
        "success_rate": "99.2%"
    }

# Error handler for 404
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "message": "Endpoint not found",
            "available_endpoints": [
                "/api",
                "/api/health", 
                "/api/dashboard",
                "/api/agents",
                "/api/voice",
                "/api/marketplace",
                "/api/inventory",
                "/api/customers",
                "/api/analytics",
                "/api/settings",
                "/api/payments"
            ]
        }
    )

# For Vercel serverless function
handler = app

# For local development
if __name__ == "__main__":
    import uvicorn
    print("🇮🇳 Starting VyapaarGPT Backend Server...")
    print("🚀 FastAPI + AI Business OS for India")
    print("📊 Available at: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/api/docs")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )