import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
from loguru import logger
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db
from app.models.schemas import Transaction, User, InventoryItem

class FinanceAgent:
    """
    AI Agent specialized in financial analysis, profitability insights,
    and business health monitoring for Indian MSMEs.
    """
    
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.name = "Financial Analysis Assistant"
        self.expertise = [
            "Profitability analysis",
            "Cash flow monitoring",
            "Expense categorization",
            "Revenue forecasting", 
            "Tax compliance insights",
            "Credit score evaluation"
        ]
        
    async def initialize(self):
        """Initialize the finance agent"""
        logger.info("💰 Initializing Finance Agent")
        # Load financial templates, tax rates, etc.
        self.expense_categories = self._load_expense_categories()
        self.tax_rates = self._load_tax_rates()
        self.financial_ratios = self._load_financial_ratios()
        
    async def process_query(
        self, 
        user_id: int, 
        query: str, 
        intent: Dict[str, Any], 
        language: str
    ) -> Dict[str, Any]:
        """Process finance-related queries"""
        try:
            entities = intent.get("entities", [])
            
            # Determine specific financial action
            if any(word in query.lower() for word in ["sales", "बिक्री", "revenue", "आय"]):
                return await self._handle_sales_inquiry(user_id, query, language)
            elif any(word in query.lower() for word in ["profit", "लाभ", "margin", "मार्जिन"]):
                return await self._handle_profit_analysis(user_id, query, language)
            elif any(word in query.lower() for word in ["expense", "खर्च", "cost", "लागत"]):
                return await self._handle_expense_analysis(user_id, query, language)
            elif any(word in query.lower() for word in ["cash", "नकदी", "flow", "फ्लो"]):
                return await self._handle_cashflow_inquiry(user_id, query, language)
            elif any(word in query.lower() for word in ["tax", "टैक्स", "gst", "जीएसटी"]):
                return await self._handle_tax_inquiry(user_id, query, language)
            else:
                return await self._handle_general_finance_query(user_id, query, language)
                
        except Exception as e:
            logger.error(f"Finance agent query processing failed: {e}")
            return {
                "text": "वित्तीय जानकारी लेने में समस्या हो रही है" if language == "hi" else "Having trouble with financial information",
                "agent": "finance",
                "success": False
            }
    
    async def get_insights(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive financial insights"""
        try:
            db = next(get_db())
            
            # Get financial data for the last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            # Get transactions
            transactions = db.query(Transaction).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_date >= thirty_days_ago
            ).all()
            
            insights = {
                "revenue": {
                    "total_sales": 0,
                    "total_transactions": 0,
                    "avg_transaction_value": 0,
                    "daily_average": 0
                },
                "profitability": {
                    "total_profit": 0,
                    "profit_margin": 0,
                    "profitable_transactions": 0
                },
                "expenses": {
                    "total_expenses": 0,
                    "expense_categories": {},
                    "largest_expense": 0
                },
                "cash_flow": {
                    "net_cash_flow": 0,
                    "cash_in": 0,
                    "cash_out": 0
                },
                "trends": {
                    "revenue_trend": "stable",
                    "growth_rate": 0
                },
                "recommendations": []
            }
            
            if transactions:
                # Calculate revenue metrics
                sales_transactions = [t for t in transactions if t.transaction_type == "sale"]
                expense_transactions = [t for t in transactions if t.transaction_type == "expense"]
                
                if sales_transactions:
                    insights["revenue"]["total_sales"] = sum(t.amount for t in sales_transactions)
                    insights["revenue"]["total_transactions"] = len(sales_transactions)
                    insights["revenue"]["avg_transaction_value"] = (
                        insights["revenue"]["total_sales"] / len(sales_transactions)
                    )
                    insights["revenue"]["daily_average"] = insights["revenue"]["total_sales"] / 30
                
                # Calculate profitability
                profitable_sales = [t for t in sales_transactions if t.profit_margin and t.profit_margin > 0]
                if profitable_sales:
                    insights["profitability"]["total_profit"] = sum(
                        t.amount * (t.profit_margin / 100) for t in profitable_sales
                    )
                    insights["profitability"]["profitable_transactions"] = len(profitable_sales)
                    if insights["revenue"]["total_sales"] > 0:
                        insights["profitability"]["profit_margin"] = (
                            (insights["profitability"]["total_profit"] / insights["revenue"]["total_sales"]) * 100
                        )
                
                # Calculate expenses
                if expense_transactions:
                    insights["expenses"]["total_expenses"] = sum(t.amount for t in expense_transactions)
                    
                    # Categorize expenses (simplified)
                    expense_categories = {}
                    for transaction in expense_transactions:
                        category = self._categorize_expense(transaction.description or "Other")
                        expense_categories[category] = expense_categories.get(category, 0) + transaction.amount
                    
                    insights["expenses"]["expense_categories"] = expense_categories
                    insights["expenses"]["largest_expense"] = max(expense_categories.values()) if expense_categories else 0
                
                # Calculate cash flow
                insights["cash_flow"]["cash_in"] = insights["revenue"]["total_sales"]
                insights["cash_flow"]["cash_out"] = insights["expenses"]["total_expenses"]
                insights["cash_flow"]["net_cash_flow"] = (
                    insights["cash_flow"]["cash_in"] - insights["cash_flow"]["cash_out"]
                )
                
                # Analyze trends (simplified)
                insights["trends"] = await self._analyze_trends(user_id, db)
            
            # Generate recommendations
            insights["recommendations"] = await self._generate_financial_recommendations(insights)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get financial insights: {e}")
            return {"error": "Failed to generate financial insights"}
    
    async def _handle_sales_inquiry(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle sales and revenue inquiries"""
        try:
            db = next(get_db())
            
            # Get sales data for different time periods
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)
            
            # Today's sales
            today_sales = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "sale",
                func.date(Transaction.transaction_date) == today
            ).scalar() or 0
            
            # Yesterday's sales
            yesterday_sales = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "sale", 
                func.date(Transaction.transaction_date) == yesterday
            ).scalar() or 0
            
            # This week's sales
            week_sales = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "sale",
                Transaction.transaction_date >= week_ago
            ).scalar() or 0
            
            # This month's sales
            month_sales = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "sale",
                Transaction.transaction_date >= month_ago
            ).scalar() or 0
            
            if language == "hi":
                sales_text = f"""
                📈 आपकी बिक्री की रिपोर्ट:
                
                आज की बिक्री: ₹{today_sales:.2f}
                कल की बिक्री: ₹{yesterday_sales:.2f}
                इस हफ्ते: ₹{week_sales:.2f}
                इस महीने: ₹{month_sales:.2f}
                
                """
                
                # Add trend analysis
                if today_sales > yesterday_sales:
                    sales_text += "📊 ट्रेंड: आज की बिक्री कल से बेहतर है! 👍\n"
                elif today_sales < yesterday_sales:
                    sales_text += "📊 ट्रेंड: आज की बिक्री कल से कम है। सुधार की जरूरत।\n"
                else:
                    sales_text += "📊 ट्रेंड: आज की बिक्री कल के बराबर है।\n"
                    
                sales_text += f"\nदैनिक औसत: ₹{month_sales/30:.2f}"
            else:
                sales_text = f"""
                📈 Your Sales Report:
                
                Today's Sales: ₹{today_sales:.2f}
                Yesterday's Sales: ₹{yesterday_sales:.2f}
                This Week: ₹{week_sales:.2f}
                This Month: ₹{month_sales:.2f}
                
                """
                
                # Add trend analysis
                if today_sales > yesterday_sales:
                    sales_text += "📊 Trend: Today's sales are better than yesterday! 👍\n"
                elif today_sales < yesterday_sales:
                    sales_text += "📊 Trend: Today's sales are lower than yesterday. Needs improvement.\n"
                else:
                    sales_text += "📊 Trend: Today's sales equal to yesterday.\n"
                    
                sales_text += f"\nDaily Average: ₹{month_sales/30:.2f}"
            
            return {
                "text": sales_text,
                "agent": "finance",
                "success": True,
                "data": {
                    "today_sales": today_sales,
                    "yesterday_sales": yesterday_sales,
                    "week_sales": week_sales,
                    "month_sales": month_sales
                }
            }
            
        except Exception as e:
            logger.error(f"Sales inquiry failed: {e}")
            return {
                "text": "बिक्री की जानकारी उपलब्ध नहीं है" if language == "hi" else "Sales information not available",
                "agent": "finance",
                "success": False
            }
    
    async def _handle_profit_analysis(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle profit and margin analysis"""
        try:
            db = next(get_db())
            
            # Get transactions with profit margins
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            profitable_transactions = db.query(Transaction).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "sale",
                Transaction.profit_margin.isnot(None),
                Transaction.transaction_date >= thirty_days_ago
            ).all()
            
            if not profitable_transactions:
                return {
                    "text": "अभी तक लाभ की जानकारी उपलब्ध नहीं है। अपनी लागत और बिक्री मूल्य जोड़ें।" if language == "hi" 
                           else "Profit information not available yet. Add your cost and selling prices.",
                    "agent": "finance",
                    "success": True
                }
            
            # Calculate profit metrics
            total_revenue = sum(t.amount for t in profitable_transactions)
            total_profit = sum(t.amount * (t.profit_margin / 100) for t in profitable_transactions)
            avg_profit_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0
            
            # Find best and worst performing items
            profit_by_item = {}
            for transaction in profitable_transactions:
                if transaction.items_sold:
                    items = transaction.items_sold if isinstance(transaction.items_sold, list) else []
                    for item in items:
                        item_name = item.get("name", "Unknown")
                        item_profit = transaction.amount * (transaction.profit_margin / 100)
                        profit_by_item[item_name] = profit_by_item.get(item_name, 0) + item_profit
            
            if language == "hi":
                profit_text = f"""
                💰 लाभ विश्लेषण (पिछले 30 दिन):
                
                कुल बिक्री: ₹{total_revenue:.2f}
                कुल लाभ: ₹{total_profit:.2f}
                औसत लाभ मार्जिन: {avg_profit_margin:.1f}%
                
                """
                
                if profit_by_item:
                    best_item = max(profit_by_item.items(), key=lambda x: x[1])
                    profit_text += f"सबसे लाभदायक: {best_item[0]} (₹{best_item[1]:.2f})\n"
                
                # Add recommendations
                if avg_profit_margin < 20:
                    profit_text += "\n⚠️ सुझाव: लाभ मार्जिन कम है। कीमतें बढ़ाने या लागत कम करने पर विचार करें।"
                elif avg_profit_margin > 30:
                    profit_text += "\n✅ बहुत अच्छा! लाभ मार्जिन स्वस्थ है।"
            else:
                profit_text = f"""
                💰 Profit Analysis (Last 30 days):
                
                Total Revenue: ₹{total_revenue:.2f}
                Total Profit: ₹{total_profit:.2f}
                Average Profit Margin: {avg_profit_margin:.1f}%
                
                """
                
                if profit_by_item:
                    best_item = max(profit_by_item.items(), key=lambda x: x[1])
                    profit_text += f"Most Profitable: {best_item[0]} (₹{best_item[1]:.2f})\n"
                
                # Add recommendations
                if avg_profit_margin < 20:
                    profit_text += "\n⚠️ Recommendation: Profit margin is low. Consider increasing prices or reducing costs."
                elif avg_profit_margin > 30:
                    profit_text += "\n✅ Excellent! Profit margin is healthy."
            
            return {
                "text": profit_text,
                "agent": "finance",
                "success": True,
                "data": {
                    "total_revenue": total_revenue,
                    "total_profit": total_profit,
                    "avg_profit_margin": avg_profit_margin
                }
            }
            
        except Exception as e:
            logger.error(f"Profit analysis failed: {e}")
            return {
                "text": "लाभ विश्लेषण में समस्या हो रही है" if language == "hi" else "Having trouble with profit analysis",
                "agent": "finance",
                "success": False
            }
    
    async def _handle_expense_analysis(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle expense analysis"""
        try:
            db = next(get_db())
            
            # Get expenses for the last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            expenses = db.query(Transaction).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "expense",
                Transaction.transaction_date >= thirty_days_ago
            ).all()
            
            if not expenses:
                return {
                    "text": "अभी तक कोई खर्च दर्ज नहीं है।" if language == "hi" else "No expenses recorded yet.",
                    "agent": "finance",
                    "success": True
                }
            
            total_expenses = sum(e.amount for e in expenses)
            
            # Categorize expenses
            expense_categories = {}
            for expense in expenses:
                category = self._categorize_expense(expense.description or "Other")
                expense_categories[category] = expense_categories.get(category, 0) + expense.amount
            
            if language == "hi":
                expense_text = f"""
                💸 खर्च विश्लेषण (पिछले 30 दिन):
                
                कुल खर्च: ₹{total_expenses:.2f}
                दैनिक औसत खर्च: ₹{total_expenses/30:.2f}
                
                खर्च की श्रेणियां:
                """
                
                for category, amount in sorted(expense_categories.items(), key=lambda x: x[1], reverse=True):
                    percentage = (amount / total_expenses) * 100
                    expense_text += f"• {category}: ₹{amount:.2f} ({percentage:.1f}%)\n"
                
                # Find highest expense category
                if expense_categories:
                    highest_category = max(expense_categories.items(), key=lambda x: x[1])
                    expense_text += f"\nसबसे ज्यादा खर्च: {highest_category[0]}"
            else:
                expense_text = f"""
                💸 Expense Analysis (Last 30 days):
                
                Total Expenses: ₹{total_expenses:.2f}
                Daily Average Expense: ₹{total_expenses/30:.2f}
                
                Expense Categories:
                """
                
                for category, amount in sorted(expense_categories.items(), key=lambda x: x[1], reverse=True):
                    percentage = (amount / total_expenses) * 100
                    expense_text += f"• {category}: ₹{amount:.2f} ({percentage:.1f}%)\n"
                
                # Find highest expense category
                if expense_categories:
                    highest_category = max(expense_categories.items(), key=lambda x: x[1])
                    expense_text += f"\nHighest Expense: {highest_category[0]}"
            
            return {
                "text": expense_text,
                "agent": "finance",
                "success": True,
                "data": {
                    "total_expenses": total_expenses,
                    "expense_categories": expense_categories
                }
            }
            
        except Exception as e:
            logger.error(f"Expense analysis failed: {e}")
            return {
                "text": "खर्च विश्लेषण में समस्या हो रही है" if language == "hi" else "Having trouble with expense analysis",
                "agent": "finance",
                "success": False
            }
    
    async def _handle_cashflow_inquiry(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle cash flow inquiries"""
        # Get cash in and cash out for the month
        insights = await self.get_insights(user_id)
        cash_flow = insights.get("cash_flow", {})
        
        cash_in = cash_flow.get("cash_in", 0)
        cash_out = cash_flow.get("cash_out", 0)
        net_flow = cash_flow.get("net_cash_flow", 0)
        
        if language == "hi":
            cashflow_text = f"""
            💰 नकदी प्रवाह रिपोर्ट (30 दिन):
            
            नकदी आना: ₹{cash_in:.2f}
            नकदी जाना: ₹{cash_out:.2f}
            शुद्ध नकदी प्रवाह: ₹{net_flow:.2f}
            
            """
            
            if net_flow > 0:
                cashflow_text += "✅ अच्छा! आपका नकदी प्रवाह सकारात्मक है।"
            elif net_flow < 0:
                cashflow_text += "⚠️ चेतावनी: नकदी प्रवाह नकारात्मक है। खर्च कम करें या बिक्री बढ़ाएं।"
            else:
                cashflow_text += "📊 नकदी प्रवाह संतुलित है।"
        else:
            cashflow_text = f"""
            💰 Cash Flow Report (30 days):
            
            Cash In: ₹{cash_in:.2f}
            Cash Out: ₹{cash_out:.2f}
            Net Cash Flow: ₹{net_flow:.2f}
            
            """
            
            if net_flow > 0:
                cashflow_text += "✅ Good! Your cash flow is positive."
            elif net_flow < 0:
                cashflow_text += "⚠️ Warning: Cash flow is negative. Reduce expenses or increase sales."
            else:
                cashflow_text += "📊 Cash flow is balanced."
        
        return {
            "text": cashflow_text,
            "agent": "finance",
            "success": True,
            "data": cash_flow
        }
    
    async def _handle_tax_inquiry(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle tax-related inquiries"""
        try:
            insights = await self.get_insights(user_id)
            revenue = insights.get("revenue", {}).get("total_sales", 0)
            
            # Simplified GST calculation (assuming 18% GST for most items)
            gst_rate = 18
            gst_amount = (revenue * gst_rate) / (100 + gst_rate)
            
            if language == "hi":
                tax_text = f"""
                📋 कर की जानकारी (30 दिन):
                
                कुल बिक्री: ₹{revenue:.2f}
                अनुमानित GST (18%): ₹{gst_amount:.2f}
                
                💡 याद रखें:
                • महीने की 20 तारीख तक GST रिटर्न जमा करें
                • सभी बिल संभाल कर रखें  
                • खरीदारी पर मिले GST का फायदा उठाएं
                
                अधिक जानकारी के लिए CA से सलाह लें।
                """
            else:
                tax_text = f"""
                📋 Tax Information (30 days):
                
                Total Sales: ₹{revenue:.2f}
                Estimated GST (18%): ₹{gst_amount:.2f}
                
                💡 Remember:
                • File GST returns by 20th of every month
                • Keep all bills safely
                • Claim input GST on purchases
                
                Consult a CA for detailed advice.
                """
            
            return {
                "text": tax_text,
                "agent": "finance",
                "success": True,
                "data": {
                    "revenue": revenue,
                    "estimated_gst": gst_amount
                }
            }
            
        except Exception as e:
            logger.error(f"Tax inquiry failed: {e}")
            return {
                "text": "कर की जानकारी में समस्या हो रही है" if language == "hi" else "Having trouble with tax information",
                "agent": "finance",
                "success": False
            }
    
    async def _handle_general_finance_query(self, user_id: int, query: str, language: str) -> Dict[str, Any]:
        """Handle general finance queries"""
        return {
            "text": "मैं बिक्री, लाभ, खर्च, नकदी प्रवाह और कर की जानकारी दे सकता हूं। कुछ खास जानना चाहते हैं?" if language == "hi" 
                   else "I can provide information about sales, profit, expenses, cash flow, and taxes. What would you like to know?",
            "agent": "finance",
            "success": True
        }
    
    def _load_expense_categories(self) -> List[str]:
        """Load expense categories for Indian businesses"""
        return [
            "Rent", "Utilities", "Staff Salary", "Inventory Purchase", 
            "Transportation", "Marketing", "Maintenance", "License/Fees",
            "Insurance", "Loan EMI", "Other"
        ]
    
    def _load_tax_rates(self) -> Dict[str, float]:
        """Load Indian tax rates"""
        return {
            "GST_5": 5.0,
            "GST_12": 12.0,
            "GST_18": 18.0,
            "GST_28": 28.0,
            "Income_Tax": 30.0
        }
    
    def _load_financial_ratios(self) -> Dict[str, Dict[str, float]]:
        """Load healthy financial ratio benchmarks"""
        return {
            "profit_margin": {"good": 20, "average": 10, "poor": 5},
            "inventory_turnover": {"good": 12, "average": 6, "poor": 3},
            "cash_ratio": {"good": 0.3, "average": 0.1, "poor": 0.05}
        }
    
    def _categorize_expense(self, description: str) -> str:
        """Categorize expense based on description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["rent", "किराया"]):
            return "Rent"
        elif any(word in description_lower for word in ["electricity", "बिजली", "water", "पानी"]):
            return "Utilities"
        elif any(word in description_lower for word in ["salary", "वेतन", "staff", "कर्मचारी"]):
            return "Staff Salary"
        elif any(word in description_lower for word in ["inventory", "stock", "स्टॉक", "माल"]):
            return "Inventory Purchase"
        elif any(word in description_lower for word in ["transport", "delivery", "डिलीवरी"]):
            return "Transportation"
        elif any(word in description_lower for word in ["marketing", "advertisement", "विज्ञापन"]):
            return "Marketing"
        elif any(word in description_lower for word in ["repair", "maintenance", "मरम्मत"]):
            return "Maintenance"
        elif any(word in description_lower for word in ["license", "fee", "लाइसेंस", "फीस"]):
            return "License/Fees"
        elif any(word in description_lower for word in ["insurance", "बीमा"]):
            return "Insurance"
        elif any(word in description_lower for word in ["loan", "emi", "लोन"]):
            return "Loan EMI"
        else:
            return "Other"
    
    async def _analyze_trends(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Analyze financial trends over time"""
        try:
            # Simple trend analysis comparing last 15 days vs previous 15 days
            fifteen_days_ago = datetime.now() - timedelta(days=15)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            # Recent period sales
            recent_sales = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "sale",
                Transaction.transaction_date >= fifteen_days_ago
            ).scalar() or 0
            
            # Previous period sales
            previous_sales = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "sale",
                Transaction.transaction_date >= thirty_days_ago,
                Transaction.transaction_date < fifteen_days_ago
            ).scalar() or 0
            
            # Calculate growth rate
            if previous_sales > 0:
                growth_rate = ((recent_sales - previous_sales) / previous_sales) * 100
            else:
                growth_rate = 0
            
            # Determine trend
            if growth_rate > 10:
                trend = "growing"
            elif growth_rate < -10:
                trend = "declining"
            else:
                trend = "stable"
            
            return {
                "revenue_trend": trend,
                "growth_rate": growth_rate,
                "recent_sales": recent_sales,
                "previous_sales": previous_sales
            }
            
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return {
                "revenue_trend": "stable",
                "growth_rate": 0
            }
    
    async def _generate_financial_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate actionable financial recommendations"""
        recommendations = []
        
        # Revenue recommendations
        revenue = insights.get("revenue", {})
        if revenue.get("total_sales", 0) == 0:
            recommendations.append("Start recording all sales transactions for better financial tracking")
        elif revenue.get("avg_transaction_value", 0) < 100:
            recommendations.append("Try to increase average transaction value through upselling")
        
        # Profitability recommendations
        profitability = insights.get("profitability", {})
        profit_margin = profitability.get("profit_margin", 0)
        if profit_margin < 15:
            recommendations.append("Consider increasing prices or reducing costs to improve profit margins")
        elif profit_margin > 35:
            recommendations.append("Excellent profit margins! Consider reinvesting in business growth")
        
        # Cash flow recommendations
        cash_flow = insights.get("cash_flow", {})
        net_flow = cash_flow.get("net_cash_flow", 0)
        if net_flow < 0:
            recommendations.append("Focus on reducing expenses and increasing sales to improve cash flow")
        
        # Expense recommendations
        expenses = insights.get("expenses", {})
        if expenses.get("total_expenses", 0) > revenue.get("total_sales", 0) * 0.8:
            recommendations.append("Expenses are high relative to revenue. Review and optimize costs")
        
        # Default recommendations
        if not recommendations:
            recommendations.extend([
                "Maintain detailed records of all transactions",
                "Review financial performance weekly",
                "Plan for seasonal variations in business"
            ])
        
        return recommendations[:5]  # Return top 5 recommendations