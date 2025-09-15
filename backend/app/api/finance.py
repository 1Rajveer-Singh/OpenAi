from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.models.database import get_db
from app.models.schemas import User, Transaction, Customer
from app.api.auth import get_current_user

router = APIRouter()

class TransactionCreate(BaseModel):
    transaction_type: str  # sale, purchase, expense, refund
    amount: float
    payment_method: str  # cash, upi, card
    upi_transaction_id: Optional[str] = None
    description: Optional[str] = None
    items_sold: Optional[List[dict]] = None
    profit_margin: Optional[float] = None
    customer_id: Optional[int] = None

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category: Optional[str] = None
    payment_method: str = "cash"

@router.get("/transactions")
async def get_transactions(
    transaction_type: Optional[str] = None,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get financial transactions"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= start_date
    )
    
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    transactions = query.order_by(Transaction.transaction_date.desc()).all()
    
    return {
        "transactions": [
            {
                "id": transaction.id,
                "transaction_type": transaction.transaction_type,
                "amount": transaction.amount,
                "payment_method": transaction.payment_method,
                "upi_transaction_id": transaction.upi_transaction_id,
                "description": transaction.description,
                "items_sold": transaction.items_sold,
                "profit_margin": transaction.profit_margin,
                "customer_id": transaction.customer_id,
                "transaction_date": transaction.transaction_date
            }
            for transaction in transactions
        ],
        "total_transactions": len(transactions),
        "date_range": f"Last {days} days"
    }

@router.post("/transactions")
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new financial transaction"""
    
    # Validate customer if provided
    if transaction_data.customer_id:
        customer = db.query(Customer).filter(
            Customer.id == transaction_data.customer_id,
            Customer.business_owner_id == current_user.id
        ).first()
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
    
    # Create new transaction
    new_transaction = Transaction(
        transaction_type=transaction_data.transaction_type,
        amount=transaction_data.amount,
        payment_method=transaction_data.payment_method,
        upi_transaction_id=transaction_data.upi_transaction_id,
        description=transaction_data.description,
        items_sold=transaction_data.items_sold,
        profit_margin=transaction_data.profit_margin,
        customer_id=transaction_data.customer_id,
        user_id=current_user.id
    )
    
    db.add(new_transaction)
    
    # Update customer data if it's a sale
    if transaction_data.transaction_type == "sale" and transaction_data.customer_id:
        customer = db.query(Customer).filter(Customer.id == transaction_data.customer_id).first()
        if customer:
            customer.total_purchases += transaction_data.amount
            customer.last_purchase_date = datetime.now()
            
            # Award loyalty points (1 point per ₹10 spent)
            points_earned = int(transaction_data.amount / 10)
            customer.loyalty_points += points_earned
    
    db.commit()
    db.refresh(new_transaction)
    
    return {
        "message": "Transaction created successfully",
        "transaction": {
            "id": new_transaction.id,
            "transaction_type": new_transaction.transaction_type,
            "amount": new_transaction.amount,
            "payment_method": new_transaction.payment_method,
            "transaction_date": new_transaction.transaction_date
        }
    }

@router.get("/sales-report")
async def get_sales_report(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive sales report"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get sales transactions
    sales = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "sale",
        Transaction.transaction_date >= start_date
    ).all()
    
    if not sales:
        return {
            "report": {
                "total_sales": 0,
                "total_transactions": 0,
                "avg_transaction_value": 0,
                "daily_average": 0,
                "payment_methods": {},
                "profit_analysis": {}
            }
        }
    
    # Calculate metrics
    total_sales = sum(sale.amount for sale in sales)
    total_transactions = len(sales)
    avg_transaction_value = total_sales / total_transactions
    daily_average = total_sales / days
    
    # Payment method breakdown
    payment_methods = {}
    for sale in sales:
        method = sale.payment_method
        if method in payment_methods:
            payment_methods[method]["count"] += 1
            payment_methods[method]["amount"] += sale.amount
        else:
            payment_methods[method] = {"count": 1, "amount": sale.amount}
    
    # Profit analysis
    profitable_sales = [s for s in sales if s.profit_margin]
    total_profit = sum(s.amount * (s.profit_margin / 100) for s in profitable_sales)
    avg_profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    
    # Daily sales breakdown
    daily_sales = {}
    for sale in sales:
        date_key = sale.transaction_date.date().isoformat()
        if date_key in daily_sales:
            daily_sales[date_key] += sale.amount
        else:
            daily_sales[date_key] = sale.amount
    
    return {
        "report": {
            "period": f"Last {days} days",
            "total_sales": total_sales,
            "total_transactions": total_transactions,
            "avg_transaction_value": avg_transaction_value,
            "daily_average": daily_average,
            "payment_methods": payment_methods,
            "profit_analysis": {
                "total_profit": total_profit,
                "avg_profit_margin": avg_profit_margin,
                "profitable_transactions": len(profitable_sales)
            },
            "daily_breakdown": daily_sales
        }
    }

@router.get("/expense-report")
async def get_expense_report(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive expense report"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get expense transactions
    expenses = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= start_date
    ).all()
    
    if not expenses:
        return {
            "report": {
                "total_expenses": 0,
                "total_transactions": 0,
                "avg_expense": 0,
                "daily_average": 0,
                "categories": {}
            }
        }
    
    # Calculate metrics
    total_expenses = sum(expense.amount for expense in expenses)
    total_transactions = len(expenses)
    avg_expense = total_expenses / total_transactions
    daily_average = total_expenses / days
    
    # Categorize expenses (simplified categorization)
    categories = {}
    for expense in expenses:
        category = expense.description or "Uncategorized"
        
        # Simple categorization based on keywords
        if any(word in category.lower() for word in ["rent", "किराया"]):
            category = "Rent"
        elif any(word in category.lower() for word in ["salary", "वेतन"]):
            category = "Staff Salary"
        elif any(word in category.lower() for word in ["electricity", "बिजली"]):
            category = "Utilities"
        elif any(word in category.lower() for word in ["inventory", "stock"]):
            category = "Inventory"
        else:
            category = "Other"
        
        if category in categories:
            categories[category]["count"] += 1
            categories[category]["amount"] += expense.amount
        else:
            categories[category] = {"count": 1, "amount": expense.amount}
    
    return {
        "report": {
            "period": f"Last {days} days",
            "total_expenses": total_expenses,
            "total_transactions": total_transactions,
            "avg_expense": avg_expense,
            "daily_average": daily_average,
            "categories": categories
        }
    }

@router.get("/profit-loss")
async def get_profit_loss_statement(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get profit and loss statement"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get revenue (sales)
    sales = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "sale",
        Transaction.transaction_date >= start_date
    ).scalar() or 0
    
    # Get expenses
    expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= start_date
    ).scalar() or 0
    
    # Calculate metrics
    gross_profit = sales - expenses
    profit_margin = (gross_profit / sales) * 100 if sales > 0 else 0
    
    return {
        "statement": {
            "period": f"Last {days} days",
            "revenue": {
                "total_sales": sales,
                "description": "Total sales revenue"
            },
            "expenses": {
                "total_expenses": expenses,
                "description": "Total business expenses"
            },
            "profit": {
                "gross_profit": gross_profit,
                "profit_margin": profit_margin,
                "status": "profit" if gross_profit > 0 else "loss"
            }
        }
    }

@router.get("/cash-flow")
async def get_cash_flow_analysis(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get cash flow analysis"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Cash inflows (sales)
    cash_in = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "sale",
        Transaction.transaction_date >= start_date
    ).scalar() or 0
    
    # Cash outflows (expenses, purchases)
    cash_out = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type.in_(["expense", "purchase"]),
        Transaction.transaction_date >= start_date
    ).scalar() or 0
    
    # Net cash flow
    net_cash_flow = cash_in - cash_out
    
    # Daily cash flow breakdown
    daily_cash_flow = {}
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).date()
        
        daily_in = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "sale",
            func.date(Transaction.transaction_date) == date
        ).scalar() or 0
        
        daily_out = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type.in_(["expense", "purchase"]),
            func.date(Transaction.transaction_date) == date
        ).scalar() or 0
        
        daily_cash_flow[date.isoformat()] = {
            "cash_in": daily_in,
            "cash_out": daily_out,
            "net_flow": daily_in - daily_out
        }
    
    return {
        "cash_flow": {
            "period": f"Last {days} days",
            "summary": {
                "total_cash_in": cash_in,
                "total_cash_out": cash_out,
                "net_cash_flow": net_cash_flow,
                "cash_flow_status": "positive" if net_cash_flow > 0 else "negative"
            },
            "daily_breakdown": daily_cash_flow
        }
    }

@router.post("/expenses")
async def add_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new expense transaction"""
    
    new_expense = Transaction(
        transaction_type="expense",
        amount=expense_data.amount,
        payment_method=expense_data.payment_method,
        description=expense_data.description,
        user_id=current_user.id
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return {
        "message": "Expense added successfully",
        "expense": {
            "id": new_expense.id,
            "amount": new_expense.amount,
            "description": new_expense.description,
            "payment_method": new_expense.payment_method,
            "transaction_date": new_expense.transaction_date
        }
    }

@router.get("/dashboard")
async def get_financial_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get financial dashboard with key metrics"""
    
    # Today's metrics
    today = datetime.now().date()
    
    today_sales = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "sale",
        func.date(Transaction.transaction_date) == today
    ).scalar() or 0
    
    today_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        func.date(Transaction.transaction_date) == today
    ).scalar() or 0
    
    # This month's metrics
    month_start = datetime.now().replace(day=1)
    
    month_sales = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "sale",
        Transaction.transaction_date >= month_start
    ).scalar() or 0
    
    month_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= month_start
    ).scalar() or 0
    
    return {
        "dashboard": {
            "today": {
                "sales": today_sales,
                "expenses": today_expenses,
                "net_profit": today_sales - today_expenses
            },
            "this_month": {
                "sales": month_sales,
                "expenses": month_expenses,
                "net_profit": month_sales - month_expenses,
                "profit_margin": ((month_sales - month_expenses) / month_sales) * 100 if month_sales > 0 else 0
            },
            "quick_stats": {
                "avg_daily_sales": month_sales / datetime.now().day,
                "avg_daily_expenses": month_expenses / datetime.now().day
            }
        }
    }