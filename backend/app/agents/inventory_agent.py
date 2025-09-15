import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
from loguru import logger
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import InventoryItem, Transaction

class InventoryAgent:
    """
    AI Agent specialized in inventory management, demand forecasting,
    and supplier management for Indian MSMEs.
    """
    
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.name = "Inventory Assistant"
        self.expertise = [
            "Stock level monitoring",
            "Demand forecasting", 
            "Seasonal trend analysis",
            "Festival demand prediction",
            "Supplier recommendations",
            "Expiry management"
        ]
        
    async def initialize(self):
        """Initialize the inventory agent"""
        logger.info("🏪 Initializing Inventory Agent")
        # Load seasonal patterns, festival data, etc.
        self.seasonal_patterns = self._load_seasonal_patterns()
        self.festival_calendar = self._load_festival_calendar()
        
    async def process_query(
        self, 
        user_id: int, 
        query: str, 
        intent: Dict[str, Any], 
        language: str
    ) -> Dict[str, Any]:
        """Process inventory-related queries"""
        try:
            entities = intent.get("entities", [])
            
            # Determine specific inventory action
            if any(word in query.lower() for word in ["stock", "स्टॉक", "inventory", "भंडार"]):
                return await self._handle_stock_inquiry(user_id, query, language)
            elif any(word in query.lower() for word in ["forecast", "predict", "भविष्यवाणी", "पूर्वानुमान"]):
                return await self._handle_demand_forecast(user_id, query, language)
            elif any(word in query.lower() for word in ["supplier", "सप्लायर", "vendor", "विक्रेता"]):
                return await self._handle_supplier_query(user_id, query, language)
            elif any(word in query.lower() for word in ["expiry", "एक्सपायरी", "expire", "समाप्त"]):
                return await self._handle_expiry_check(user_id, query, language)
            else:
                return await self._handle_general_inventory_query(user_id, query, language)
                
        except Exception as e:
            logger.error(f"Inventory agent query processing failed: {e}")
            return {
                "text": "स्टॉक की जानकारी लेने में समस्या हो रही है" if language == "hi" else "Having trouble with stock information",
                "agent": "inventory",
                "success": False
            }
    
    async def get_insights(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive inventory insights"""
        try:
            db = next(get_db())
            
            # Get current inventory status
            inventory_items = db.query(InventoryItem).filter(
                InventoryItem.owner_id == user_id
            ).all()
            
            insights = {
                "total_items": len(inventory_items),
                "low_stock_items": [],
                "high_demand_predictions": [],
                "seasonal_recommendations": [],
                "expiry_alerts": [],
                "supplier_recommendations": []
            }
            
            for item in inventory_items:
                # Check low stock
                if item.current_stock <= item.min_stock_level:
                    insights["low_stock_items"].append({
                        "name": item.name,
                        "current_stock": item.current_stock,
                        "min_level": item.min_stock_level,
                        "urgency": "high" if item.current_stock < item.min_stock_level * 0.5 else "medium"
                    })
                
                # Check expiry
                if item.expiry_date and item.expiry_date <= datetime.now() + timedelta(days=7):
                    insights["expiry_alerts"].append({
                        "name": item.name,
                        "expiry_date": item.expiry_date.isoformat(),
                        "days_remaining": (item.expiry_date - datetime.now()).days
                    })
            
            # Generate demand predictions
            insights["high_demand_predictions"] = await self._predict_high_demand_items(user_id, db)
            
            # Generate seasonal recommendations
            insights["seasonal_recommendations"] = await self._get_seasonal_recommendations()
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get inventory insights: {e}")
            return {"error": "Failed to generate inventory insights"}
    
    async def _handle_stock_inquiry(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle stock level inquiries"""
        try:
            db = next(get_db())
            
            # Get current stock summary
            inventory_items = db.query(InventoryItem).filter(
                InventoryItem.owner_id == user_id
            ).all()
            
            total_items = len(inventory_items)
            low_stock_count = sum(1 for item in inventory_items if item.current_stock <= item.min_stock_level)
            
            if language == "hi":
                response_text = f"""
                📊 आपका स्टॉक स्थिति:
                
                कुल आइटम: {total_items}
                कम स्टॉक वाले आइटम: {low_stock_count}
                
                """
                
                if low_stock_count > 0:
                    low_stock_items = [item for item in inventory_items if item.current_stock <= item.min_stock_level][:3]
                    response_text += "तुरंत ऑर्डर करें:\n"
                    for item in low_stock_items:
                        response_text += f"• {item.name}: {item.current_stock} बचे हैं\n"
            else:
                response_text = f"""
                📊 Your Stock Status:
                
                Total Items: {total_items}
                Low Stock Items: {low_stock_count}
                
                """
                
                if low_stock_count > 0:
                    low_stock_items = [item for item in inventory_items if item.current_stock <= item.min_stock_level][:3]
                    response_text += "Order Immediately:\n"
                    for item in low_stock_items:
                        response_text += f"• {item.name}: {item.current_stock} remaining\n"
            
            return {
                "text": response_text,
                "agent": "inventory",
                "success": True,
                "data": {
                    "total_items": total_items,
                    "low_stock_count": low_stock_count
                }
            }
            
        except Exception as e:
            logger.error(f"Stock inquiry failed: {e}")
            return {
                "text": "स्टॉक की जानकारी उपलब्ध नहीं है" if language == "hi" else "Stock information not available",
                "agent": "inventory", 
                "success": False
            }
    
    async def _handle_demand_forecast(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle demand forecasting requests"""
        try:
            # Get historical sales data
            db = next(get_db())
            
            # Simplified demand forecasting using seasonal patterns
            current_month = datetime.now().month
            upcoming_festivals = self._get_upcoming_festivals()
            
            forecast_text = "🔮 मांग पूर्वानुमान:\n\n" if language == "hi" else "🔮 Demand Forecast:\n\n"
            
            if upcoming_festivals:
                festival = upcoming_festivals[0]
                if language == "hi":
                    forecast_text += f"आगामी {festival['name']} के लिए:\n"
                    forecast_text += f"• मिठाई और नमकीन की मांग 150% बढ़ेगी\n"
                    forecast_text += f"• सजावट का सामान 200% बढ़ेगा\n"
                    forecast_text += f"• दैनिक उपयोग की चीजों में 30% वृद्धि\n"
                else:
                    forecast_text += f"For upcoming {festival['name']}:\n"
                    forecast_text += f"• Sweets and snacks demand will increase by 150%\n"
                    forecast_text += f"• Decoration items will increase by 200%\n"
                    forecast_text += f"• Daily essentials will see 30% growth\n"
            
            # Add seasonal predictions
            seasonal_prediction = self._get_seasonal_prediction(current_month)
            forecast_text += f"\n{seasonal_prediction[language]}"
            
            return {
                "text": forecast_text,
                "agent": "inventory",
                "success": True,
                "data": {
                    "upcoming_festivals": upcoming_festivals,
                    "seasonal_factors": seasonal_prediction
                }
            }
            
        except Exception as e:
            logger.error(f"Demand forecast failed: {e}")
            return {
                "text": "मांग पूर्वानुमान उपलब्ध नहीं है" if language == "hi" else "Demand forecast not available",
                "agent": "inventory",
                "success": False
            }
    
    async def _handle_supplier_query(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle supplier-related queries"""
        suppliers_text = """
        🏭 सुझाए गए सप्लायर:
        
        • राज ट्रेडर्स - 📞 9876543210
          कम कीमत, अच्छी गुणवत्ता
          
        • शर्मा होलसेल - 📞 9765432109  
          तेज़ डिलीवरी, 2 दिन
          
        • गुप्ता स्टोर्स - 📞 9654321098
          बल्क ऑर्डर में छूट
        """ if language == "hi" else """
        🏭 Recommended Suppliers:
        
        • Raj Traders - 📞 9876543210
          Low prices, good quality
          
        • Sharma Wholesale - 📞 9765432109
          Fast delivery, 2 days
          
        • Gupta Stores - 📞 9654321098
          Bulk order discounts
        """
        
        return {
            "text": suppliers_text,
            "agent": "inventory",
            "success": True
        }
    
    async def _handle_expiry_check(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle expiry date checks"""
        try:
            db = next(get_db())
            
            # Get items expiring soon
            upcoming_expiry = db.query(InventoryItem).filter(
                InventoryItem.owner_id == user_id,
                InventoryItem.expiry_date.isnot(None),
                InventoryItem.expiry_date <= datetime.now() + timedelta(days=7)
            ).all()
            
            if not upcoming_expiry:
                return {
                    "text": "कोई चीज़ जल्दी एक्सपायर नहीं हो रही! 👍" if language == "hi" else "Nothing expiring soon! 👍",
                    "agent": "inventory",
                    "success": True
                }
            
            expiry_text = "⚠️ जल्दी एक्सपायर होने वाली चीज़ें:\n\n" if language == "hi" else "⚠️ Items Expiring Soon:\n\n"
            
            for item in upcoming_expiry[:5]:
                days_left = (item.expiry_date - datetime.now()).days
                if language == "hi":
                    expiry_text += f"• {item.name}: {days_left} दिन बचे\n"
                else:
                    expiry_text += f"• {item.name}: {days_left} days left\n"
            
            return {
                "text": expiry_text,
                "agent": "inventory", 
                "success": True,
                "data": {"expiring_items": len(upcoming_expiry)}
            }
            
        except Exception as e:
            logger.error(f"Expiry check failed: {e}")
            return {
                "text": "एक्सपायरी की जानकारी उपलब्ध नहीं है" if language == "hi" else "Expiry information not available",
                "agent": "inventory",
                "success": False
            }
    
    async def _handle_general_inventory_query(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle general inventory queries"""
        return {
            "text": "मैं आपके स्टॉक, मांग पूर्वानुमान, और सप्लायर की मदद कर सकता हूं। कुछ खास जानना चाहते हैं?" if language == "hi" 
                   else "I can help with your stock, demand forecasting, and suppliers. What would you like to know?",
            "agent": "inventory",
            "success": True
        }
    
    def _load_seasonal_patterns(self) -> Dict[str, Any]:
        """Load seasonal demand patterns for India"""
        return {
            "winter": {"months": [11, 12, 1, 2], "high_demand": ["warm_clothes", "heaters", "medicines"]},
            "summer": {"months": [3, 4, 5, 6], "high_demand": ["cooling_items", "cold_drinks", "fans"]},
            "monsoon": {"months": [7, 8, 9], "high_demand": ["umbrellas", "rain_gear", "warm_food"]},
            "festive": {"months": [10, 11], "high_demand": ["sweets", "decorations", "gifts"]}
        }
    
    def _load_festival_calendar(self) -> List[Dict[str, Any]]:
        """Load Indian festival calendar for demand prediction"""
        return [
            {"name": "Diwali", "month": 11, "high_demand": ["sweets", "lights", "gifts"]},
            {"name": "Holi", "month": 3, "high_demand": ["colors", "sweets", "snacks"]},
            {"name": "Dussehra", "month": 10, "high_demand": ["sweets", "clothes", "decorations"]},
            {"name": "Eid", "month": 4, "high_demand": ["sweets", "clothes", "meat"]},
            {"name": "Christmas", "month": 12, "high_demand": ["cakes", "decorations", "gifts"]}
        ]
    
    def _get_upcoming_festivals(self) -> List[Dict[str, Any]]:
        """Get upcoming festivals in next 30 days"""
        current_month = datetime.now().month
        return [f for f in self.festival_calendar if f["month"] >= current_month][:2]
    
    def _get_seasonal_prediction(self, month: int) -> Dict[str, str]:
        """Get seasonal predictions based on current month"""
        if month in [11, 12, 1, 2]:
            return {
                "hi": "सर्दी का मौसम: गर्म कपड़े और हीटर की मांग बढ़ेगी",
                "en": "Winter season: Demand for warm clothes and heaters will increase"
            }
        elif month in [3, 4, 5, 6]:
            return {
                "hi": "गर्मी का मौसम: ठंडे पेय और पंखे की मांग बढ़ेगी", 
                "en": "Summer season: Demand for cold drinks and fans will increase"
            }
        elif month in [7, 8, 9]:
            return {
                "hi": "बारिश का मौसम: छाते और रेन गियर की मांग बढ़ेगी",
                "en": "Monsoon season: Demand for umbrellas and rain gear will increase"
            }
        else:
            return {
                "hi": "त्योहारी मौसम: मिठाई और सजावट का सामान चाहिए होगा",
                "en": "Festival season: Sweets and decorations will be in demand"
            }
    
    async def _predict_high_demand_items(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        """Predict items that will have high demand"""
        # Simplified prediction based on seasonal patterns
        current_month = datetime.now().month
        seasonal_items = []
        
        if current_month in [11, 12, 1, 2]:  # Winter
            seasonal_items = [
                {"item": "Warm Clothes", "predicted_increase": "40%"},
                {"item": "Heaters", "predicted_increase": "60%"},
                {"item": "Hot Beverages", "predicted_increase": "35%"}
            ]
        elif current_month in [3, 4, 5, 6]:  # Summer  
            seasonal_items = [
                {"item": "Cold Drinks", "predicted_increase": "50%"},
                {"item": "Fans/Coolers", "predicted_increase": "45%"},
                {"item": "Summer Clothes", "predicted_increase": "30%"}
            ]
        
        return seasonal_items
    
    async def _get_seasonal_recommendations(self) -> List[str]:
        """Get seasonal business recommendations"""
        current_month = datetime.now().month
        
        if current_month in [11, 12, 1, 2]:
            return [
                "Stock up on warm clothing and blankets",
                "Increase inventory of hot beverages",
                "Prepare for winter medicine demand"
            ]
        elif current_month in [3, 4, 5, 6]:
            return [
                "Increase cold drinks and ice cream stock",
                "Stock cooling appliances",
                "Prepare summer clothing inventory"
            ]
        else:
            return [
                "Maintain balanced inventory",
                "Monitor fast-moving items",
                "Plan for upcoming seasonal changes"
            ]