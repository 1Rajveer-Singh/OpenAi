import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
from loguru import logger
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import Customer, Transaction

class CustomerAgent:
    """
    AI Agent specialized in customer engagement, loyalty management,
    and personalized marketing for Indian MSMEs.
    """
    
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.name = "Customer Engagement Assistant"
        self.expertise = [
            "Customer segmentation",
            "Personalized promotions",
            "WhatsApp marketing automation", 
            "Loyalty program management",
            "Customer behavior analysis",
            "Retention strategies"
        ]
        
    async def initialize(self):
        """Initialize the customer agent"""
        logger.info("👥 Initializing Customer Agent")
        # Load customer behavior patterns, promotion templates
        self.promotion_templates = self._load_promotion_templates()
        self.customer_segments = self._load_customer_segments()
        
    async def process_query(
        self, 
        user_id: int, 
        query: str, 
        intent: Dict[str, Any], 
        language: str
    ) -> Dict[str, Any]:
        """Process customer-related queries"""
        try:
            entities = intent.get("entities", [])
            
            # Determine specific customer action
            if any(word in query.lower() for word in ["customer", "ग्राहक", "खरीदार"]):
                return await self._handle_customer_inquiry(user_id, query, language)
            elif any(word in query.lower() for word in ["promotion", "प्रमोशन", "offer", "ऑफर"]):
                return await self._handle_promotion_request(user_id, query, language)
            elif any(word in query.lower() for word in ["loyalty", "वफादारी", "points", "पॉइंट्स"]):
                return await self._handle_loyalty_query(user_id, query, language)
            elif any(word in query.lower() for word in ["whatsapp", "व्हाट्सऐप", "message", "संदेश"]):
                return await self._handle_whatsapp_marketing(user_id, query, language)
            else:
                return await self._handle_general_customer_query(user_id, query, language)
                
        except Exception as e:
            logger.error(f"Customer agent query processing failed: {e}")
            return {
                "text": "ग्राहक की जानकारी लेने में समस्या हो रही है" if language == "hi" else "Having trouble with customer information",
                "agent": "customer",
                "success": False
            }
    
    async def get_insights(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive customer insights"""
        try:
            db = next(get_db())
            
            # Get customer data
            customers = db.query(Customer).filter(
                Customer.business_owner_id == user_id
            ).all()
            
            insights = {
                "total_customers": len(customers),
                "top_customers": [],
                "customer_segments": {
                    "regular": 0,
                    "premium": 0, 
                    "occasional": 0
                },
                "engagement_metrics": {
                    "avg_engagement_score": 0,
                    "active_customers": 0,
                    "inactive_customers": 0
                },
                "loyalty_program": {
                    "total_points_issued": 0,
                    "active_participants": 0
                },
                "recommendations": []
            }
            
            if customers:
                # Segment customers
                for customer in customers:
                    if customer.customer_type in insights["customer_segments"]:
                        insights["customer_segments"][customer.customer_type] += 1
                
                # Calculate engagement metrics
                total_engagement = sum(c.engagement_score for c in customers if c.engagement_score)
                insights["engagement_metrics"]["avg_engagement_score"] = (
                    total_engagement / len(customers) if customers else 0
                )
                
                # Find top customers by purchase value
                top_customers = sorted(customers, key=lambda x: x.total_purchases, reverse=True)[:5]
                insights["top_customers"] = [
                    {
                        "name": customer.name,
                        "total_purchases": customer.total_purchases,
                        "loyalty_points": customer.loyalty_points,
                        "last_purchase": customer.last_purchase_date.isoformat() if customer.last_purchase_date else None
                    }
                    for customer in top_customers
                ]
                
                # Calculate loyalty metrics
                insights["loyalty_program"]["total_points_issued"] = sum(c.loyalty_points for c in customers)
                insights["loyalty_program"]["active_participants"] = sum(1 for c in customers if c.loyalty_points > 0)
                
                # Active vs inactive customers (purchased in last 30 days)
                thirty_days_ago = datetime.now() - timedelta(days=30)
                insights["engagement_metrics"]["active_customers"] = sum(
                    1 for c in customers 
                    if c.last_purchase_date and c.last_purchase_date >= thirty_days_ago
                )
                insights["engagement_metrics"]["inactive_customers"] = (
                    len(customers) - insights["engagement_metrics"]["active_customers"]
                )
            
            # Generate recommendations
            insights["recommendations"] = await self._generate_customer_recommendations(insights, user_id)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get customer insights: {e}")
            return {"error": "Failed to generate customer insights"}
    
    async def _handle_customer_inquiry(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle customer information inquiries"""
        try:
            db = next(get_db())
            
            customers = db.query(Customer).filter(
                Customer.business_owner_id == user_id
            ).all()
            
            total_customers = len(customers)
            
            # Calculate customer metrics
            if customers:
                regular_customers = sum(1 for c in customers if c.customer_type == "regular")
                premium_customers = sum(1 for c in customers if c.customer_type == "premium")
                
                # Recent customers (last 7 days)
                recent_customers = sum(
                    1 for c in customers 
                    if c.created_at >= datetime.now() - timedelta(days=7)
                )
                
                if language == "hi":
                    response_text = f"""
                    👥 आपके ग्राहक की जानकारी:
                    
                    कुल ग्राहक: {total_customers}
                    नियमित ग्राहक: {regular_customers}
                    प्रीमियम ग्राहक: {premium_customers}
                    नए ग्राहक (7 दिन): {recent_customers}
                    
                    """
                    
                    if customers:
                        top_customer = max(customers, key=lambda x: x.total_purchases)
                        response_text += f"सबसे अच्छे ग्राहक: {top_customer.name}\n"
                        response_text += f"उनकी खरीदारी: ₹{top_customer.total_purchases:.2f}\n"
                else:
                    response_text = f"""
                    👥 Your Customer Information:
                    
                    Total Customers: {total_customers}
                    Regular Customers: {regular_customers}
                    Premium Customers: {premium_customers}
                    New Customers (7 days): {recent_customers}
                    
                    """
                    
                    if customers:
                        top_customer = max(customers, key=lambda x: x.total_purchases)
                        response_text += f"Top Customer: {top_customer.name}\n"
                        response_text += f"Their Purchases: ₹{top_customer.total_purchases:.2f}\n"
            else:
                response_text = "अभी तक कोई ग्राहक डेटा उपलब्ध नहीं है" if language == "hi" else "No customer data available yet"
            
            return {
                "text": response_text,
                "agent": "customer",
                "success": True,
                "data": {
                    "total_customers": total_customers
                }
            }
            
        except Exception as e:
            logger.error(f"Customer inquiry failed: {e}")
            return {
                "text": "ग्राहक की जानकारी उपलब्ध नहीं है" if language == "hi" else "Customer information not available",
                "agent": "customer",
                "success": False
            }
    
    async def _handle_promotion_request(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle promotion creation requests"""
        try:
            # Generate personalized promotion suggestions
            promotions = await self._generate_promotions(user_id, language)
            
            promotion_text = "🎉 सुझाए गए प्रमोशन:\n\n" if language == "hi" else "🎉 Suggested Promotions:\n\n"
            
            for i, promo in enumerate(promotions[:3], 1):
                promotion_text += f"{i}. {promo}\n\n"
            
            promotion_text += "कौन सा प्रमोशन भेजना चाहते हैं?" if language == "hi" else "Which promotion would you like to send?"
            
            return {
                "text": promotion_text,
                "agent": "customer",
                "success": True,
                "data": {"promotions": promotions}
            }
            
        except Exception as e:
            logger.error(f"Promotion request failed: {e}")
            return {
                "text": "प्रमोशन बनाने में समस्या हो रही है" if language == "hi" else "Having trouble creating promotions",
                "agent": "customer",
                "success": False
            }
    
    async def _handle_loyalty_query(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle loyalty program queries"""
        try:
            db = next(get_db())
            
            customers = db.query(Customer).filter(
                Customer.business_owner_id == user_id
            ).all()
            
            total_points_issued = sum(c.loyalty_points for c in customers)
            active_loyalty_customers = sum(1 for c in customers if c.loyalty_points > 0)
            
            if language == "hi":
                loyalty_text = f"""
                🏆 लॉयल्टी प्रोग्राम की स्थिति:
                
                कुल पॉइंट्स दिए गए: {total_points_issued}
                सक्रिय सदस्य: {active_loyalty_customers}
                
                नए रिवॉर्ड्स:
                • 100 पॉइंट्स = ₹10 छूट
                • 500 पॉइंट्स = ₹60 छूट  
                • 1000 पॉइंट्स = ₹150 छूट
                
                क्या आप कोई नया रिवॉर्ड जोड़ना चाहते हैं?
                """
            else:
                loyalty_text = f"""
                🏆 Loyalty Program Status:
                
                Total Points Issued: {total_points_issued}
                Active Members: {active_loyalty_customers}
                
                Reward Structure:
                • 100 Points = ₹10 Discount
                • 500 Points = ₹60 Discount
                • 1000 Points = ₹150 Discount
                
                Would you like to add a new reward?
                """
            
            return {
                "text": loyalty_text,
                "agent": "customer",
                "success": True,
                "data": {
                    "total_points": total_points_issued,
                    "active_members": active_loyalty_customers
                }
            }
            
        except Exception as e:
            logger.error(f"Loyalty query failed: {e}")
            return {
                "text": "लॉयल्टी प्रोग्राम की जानकारी उपलब्ध नहीं है" if language == "hi" else "Loyalty program information not available",
                "agent": "customer",
                "success": False
            }
    
    async def _handle_whatsapp_marketing(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle WhatsApp marketing requests"""
        try:
            # Generate WhatsApp campaign suggestions
            campaigns = await self._generate_whatsapp_campaigns(user_id, language)
            
            whatsapp_text = "📱 व्हाट्सऐप मार्केटिंग आइडिया:\n\n" if language == "hi" else "📱 WhatsApp Marketing Ideas:\n\n"
            
            for i, campaign in enumerate(campaigns[:3], 1):
                whatsapp_text += f"{i}. {campaign}\n\n"
            
            whatsapp_text += "कौन सा मैसेज भेजना चाहते हैं?" if language == "hi" else "Which message would you like to send?"
            
            return {
                "text": whatsapp_text,
                "agent": "customer", 
                "success": True,
                "data": {"campaigns": campaigns}
            }
            
        except Exception as e:
            logger.error(f"WhatsApp marketing failed: {e}")
            return {
                "text": "व्हाट्सऐप मार्केटिंग में समस्या हो रही है" if language == "hi" else "Having trouble with WhatsApp marketing",
                "agent": "customer",
                "success": False
            }
    
    async def _handle_general_customer_query(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle general customer queries"""
        return {
            "text": "मैं ग्राहकों के साथ जुड़ने, प्रमोशन बनाने, और लॉयल्टी प्रोग्राम की मदद कर सकता हूं। कुछ खास जानना चाहते हैं?" if language == "hi" 
                   else "I can help with customer engagement, creating promotions, and loyalty programs. What would you like to know?",
            "agent": "customer",
            "success": True
        }
    
    def _load_promotion_templates(self) -> List[Dict[str, Any]]:
        """Load promotion templates for different scenarios"""
        return [
            {
                "type": "seasonal",
                "hi": "🌟 मौसमी ऑफर: सभी गर्म कपड़ों पर 20% छूट! आज ही खरीदें।",
                "en": "🌟 Seasonal Offer: 20% off on all warm clothes! Buy today."
            },
            {
                "type": "loyalty",
                "hi": "🎁 खास ग्राहकों के लिए: आपके लिए विशेष 15% छूट!",
                "en": "🎁 For Special Customers: Exclusive 15% discount for you!"
            },
            {
                "type": "new_stock",
                "hi": "🆕 नया स्टॉक आया है! सबसे पहले देखने आइए।",
                "en": "🆕 New stock arrived! Come see it first."
            },
            {
                "type": "festival",
                "hi": "🪔 दिवाली का त्योहार: सभी मिठाइयों पर 25% छूट!",
                "en": "🪔 Diwali Festival: 25% off on all sweets!"
            }
        ]
    
    def _load_customer_segments(self) -> Dict[str, Any]:
        """Load customer segmentation criteria"""
        return {
            "regular": {"min_purchases": 5, "min_amount": 1000},
            "premium": {"min_purchases": 10, "min_amount": 5000},
            "occasional": {"max_purchases": 3, "max_amount": 500}
        }
    
    async def _generate_promotions(self, user_id: int, language: str) -> List[str]:
        """Generate personalized promotion messages"""
        current_month = datetime.now().month
        promotions = []
        
        # Seasonal promotions
        if current_month in [11, 12, 1, 2]:  # Winter
            promotions.append(
                "❄️ सर्दी का स्पेशल: सभी गर्म कपड़ों पर 25% छूट! आज से 3 दिन तक।" if language == "hi"
                else "❄️ Winter Special: 25% off on all warm clothes! For 3 days only."
            )
        elif current_month in [3, 4, 5]:  # Summer preparation
            promotions.append(
                "☀️ गर्मी से पहले तैयारी: सभी कूलर और फैन पर 20% छूट!" if language == "hi"
                else "☀️ Summer Prep: 20% off on all coolers and fans!"
            )
        
        # Festival promotions
        promotions.append(
            "🎉 त्योहारी धमाका: सभी मिठाइयों पर 30% छूट! जल्दी करें!" if language == "hi"
            else "🎉 Festival Blast: 30% off on all sweets! Hurry up!"
        )
        
        # Loyalty promotions
        promotions.append(
            "💎 वफादार ग्राहकों के लिए: आपके लिए खास 15% एक्स्ट्रा छूट!" if language == "hi"
            else "💎 For Loyal Customers: Special 15% extra discount for you!"
        )
        
        return promotions
    
    async def _generate_whatsapp_campaigns(self, user_id: int, language: str) -> List[str]:
        """Generate WhatsApp campaign messages"""
        campaigns = []
        
        # Good morning campaign
        campaigns.append(
            "🌅 सुप्रभात! आज क्या चाहिए? हमारे पास सब कुछ है। 📞 कॉल करें या आइए।" if language == "hi"
            else "🌅 Good Morning! What do you need today? We have everything. 📞 Call or visit us."
        )
        
        # New arrival campaign
        campaigns.append(
            "🆕 नया माल आया है! फ्रेश स्टॉक देखने आइए। पहले आओ, पहले पाओ!" if language == "hi"
            else "🆕 New stock arrived! Come see fresh inventory. First come, first served!"
        )
        
        # Reminder campaign
        campaigns.append(
            "📞 आपको कुछ चाहिए था? हम यहां हैं आपकी सेवा में। दुकान खुली है!" if language == "hi"
            else "📞 Did you need something? We're here to serve you. Shop is open!"
        )
        
        return campaigns
    
    async def _generate_customer_recommendations(self, insights: Dict[str, Any], user_id: int) -> List[str]:
        """Generate actionable customer recommendations"""
        recommendations = []
        
        total_customers = insights.get("total_customers", 0)
        active_customers = insights.get("engagement_metrics", {}).get("active_customers", 0)
        
        if total_customers == 0:
            recommendations.append("Start collecting customer information to track their preferences")
            recommendations.append("Offer loyalty points to encourage repeat visits")
        elif active_customers < total_customers * 0.3:  # Less than 30% active
            recommendations.append("Send WhatsApp reminders to inactive customers")
            recommendations.append("Create special comeback offers for inactive customers")
        
        recommendations.append("Run seasonal promotions to increase engagement")
        recommendations.append("Ask customers for WhatsApp numbers for better communication")
        
        return recommendations