import os
import requests
from typing import Dict, Any, List
from loguru import logger

class WhatsAppBusinessAPI:
    """WhatsApp Business API integration for automated messaging"""
    
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.base_url = "https://graph.facebook.com/v18.0"
        
    async def send_message(self, to_number: str, message: str, language: str = "hi") -> Dict[str, Any]:
        """Send WhatsApp message to a customer"""
        
        if not self.access_token or not self.phone_number_id:
            logger.warning("WhatsApp credentials not configured")
            return {"success": False, "error": "WhatsApp not configured"}
        
        try:
            url = f"{self.base_url}/{self.phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Clean phone number (remove spaces, dashes, etc.)
            clean_number = ''.join(filter(str.isdigit, to_number))
            if not clean_number.startswith('91'):
                clean_number = '91' + clean_number
            
            payload = {
                "messaging_product": "whatsapp",
                "to": clean_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message_id": response.json().get("messages", [{}])[0].get("id"),
                    "status": "sent"
                }
            else:
                logger.error(f"WhatsApp API error: {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            logger.error(f"WhatsApp message failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_promotion_blast(self, numbers: List[str], message: str, language: str = "hi") -> Dict[str, Any]:
        """Send promotional message to multiple customers"""
        
        results = {
            "total_sent": 0,
            "failed": 0,
            "results": []
        }
        
        for number in numbers:
            result = await self.send_message(number, message, language)
            if result["success"]:
                results["total_sent"] += 1
            else:
                results["failed"] += 1
            
            results["results"].append({
                "number": number,
                "success": result["success"],
                "message_id": result.get("message_id"),
                "error": result.get("error")
            })
        
        return results
    
    def create_promotion_message(self, business_name: str, offer_text: str, language: str = "hi") -> str:
        """Create a promotional message template"""
        
        if language == "hi":
            return f"""
🎉 {business_name} से खुशखबरी! 

{offer_text}

जल्दी करें, सीमित समय का ऑफर!

📞 अभी संपर्क करें या दुकान पर आएं।

धन्यवाद!
{business_name}
            """.strip()
        else:
            return f"""
🎉 Great news from {business_name}!

{offer_text}

Hurry up, limited time offer!

📞 Contact us now or visit our store.

Thank you!
{business_name}
            """.strip()

class UPIIntegration:
    """UPI payment integration for transaction monitoring"""
    
    def __init__(self):
        self.razorpay_key = os.getenv("RAZORPAY_KEY_ID")
        self.razorpay_secret = os.getenv("RAZORPAY_KEY_SECRET")
    
    async def fetch_upi_transactions(self, merchant_id: str, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """Fetch UPI transactions for automatic categorization"""
        
        # This would integrate with actual UPI APIs like Razorpay, PhonePe, etc.
        # For now, returning simulated data
        
        simulated_transactions = [
            {
                "transaction_id": "upi_001",
                "amount": 150.0,
                "timestamp": "2024-01-15T10:30:00Z",
                "description": "Payment from Customer A",
                "upi_id": "customer@paytm",
                "status": "success",
                "category": "sale"
            },
            {
                "transaction_id": "upi_002", 
                "amount": 75.0,
                "timestamp": "2024-01-15T11:15:00Z",
                "description": "Payment from Customer B",
                "upi_id": "customer2@gpay",
                "status": "success",
                "category": "sale"
            }
        ]
        
        return simulated_transactions
    
    def categorize_transaction(self, description: str, amount: float) -> str:
        """Categorize UPI transaction automatically"""
        
        description_lower = description.lower()
        
        # Income patterns
        if any(word in description_lower for word in ["payment", "sale", "customer", "order"]):
            return "sale"
        
        # Expense patterns
        elif any(word in description_lower for word in ["supplier", "wholesale", "purchase", "stock"]):
            return "purchase"
        elif any(word in description_lower for word in ["rent", "electricity", "bill", "utilities"]):
            return "expense"
        elif any(word in description_lower for word in ["salary", "wages", "staff"]):
            return "salary"
        
        # Default
        else:
            return "other"

class ONDCIntegration:
    """ONDC (Open Network for Digital Commerce) integration"""
    
    def __init__(self):
        self.ondc_api_key = os.getenv("ONDC_API_KEY")
        self.base_url = "https://api.ondc.org"  # Hypothetical ONDC API
    
    async def list_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """List product on ONDC network"""
        
        try:
            # Simulate ONDC listing
            listing_response = {
                "success": True,
                "product_id": f"ondc_{product_data['sku']}",
                "listing_status": "active",
                "network_visibility": "nationwide",
                "commission_rate": 0.03  # 3% for ONDC
            }
            
            logger.info(f"Product listed on ONDC: {product_data['name']}")
            return listing_response
            
        except Exception as e:
            logger.error(f"ONDC listing failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def sync_inventory(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync inventory with ONDC network"""
        
        sync_results = {
            "total_products": len(products),
            "synced": 0,
            "failed": 0,
            "results": []
        }
        
        for product in products:
            try:
                # Simulate inventory sync
                result = await self.list_product(product)
                if result["success"]:
                    sync_results["synced"] += 1
                else:
                    sync_results["failed"] += 1
                
                sync_results["results"].append({
                    "product_name": product["name"],
                    "success": result["success"],
                    "product_id": result.get("product_id")
                })
                
            except Exception as e:
                sync_results["failed"] += 1
                sync_results["results"].append({
                    "product_name": product["name"],
                    "success": False,
                    "error": str(e)
                })
        
        return sync_results

class MarketplaceAggregator:
    """Aggregator for multiple marketplace integrations"""
    
    def __init__(self):
        self.ondc = ONDCIntegration()
        self.marketplaces = {
            "ondc": self.ondc,
            # "flipkart": FlipkartAPI(),  # Would be implemented
            # "amazon": AmazonMWSAPI(),   # Would be implemented  
            # "meesho": MeeshoAPI()       # Would be implemented
        }
    
    async def sync_product_to_marketplace(self, marketplace: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sync single product to specified marketplace"""
        
        if marketplace not in self.marketplaces:
            return {"success": False, "error": f"Marketplace {marketplace} not supported"}
        
        try:
            marketplace_api = self.marketplaces[marketplace]
            
            if marketplace == "ondc":
                return await marketplace_api.list_product(product_data)
            else:
                # For other marketplaces, would implement specific logic
                return {"success": True, "message": f"Product synced to {marketplace}"}
                
        except Exception as e:
            logger.error(f"Marketplace sync failed for {marketplace}: {e}")
            return {"success": False, "error": str(e)}
    
    async def bulk_sync_products(self, products: List[Dict[str, Any]], target_marketplaces: List[str]) -> Dict[str, Any]:
        """Sync multiple products to multiple marketplaces"""
        
        results = {
            "total_products": len(products),
            "total_marketplaces": len(target_marketplaces),
            "marketplace_results": {}
        }
        
        for marketplace in target_marketplaces:
            marketplace_results = {
                "synced": 0,
                "failed": 0,
                "product_results": []
            }
            
            for product in products:
                result = await self.sync_product_to_marketplace(marketplace, product)
                
                if result["success"]:
                    marketplace_results["synced"] += 1
                else:
                    marketplace_results["failed"] += 1
                
                marketplace_results["product_results"].append({
                    "product_name": product["name"],
                    "success": result["success"],
                    "error": result.get("error")
                })
            
            results["marketplace_results"][marketplace] = marketplace_results
        
        return results

# Initialize global instances
whatsapp_api = WhatsAppBusinessAPI()
upi_integration = UPIIntegration()
ondc_integration = ONDCIntegration()
marketplace_aggregator = MarketplaceAggregator()