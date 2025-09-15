from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.models.database import get_db
from app.models.schemas import User, Customer, Transaction
from app.api.auth import get_current_user

router = APIRouter()

class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    whatsapp_number: Optional[str] = None
    address: Optional[str] = None
    customer_type: str = "regular"  # regular, premium, occasional

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp_number: Optional[str] = None
    address: Optional[str] = None
    customer_type: Optional[str] = None

class PromotionMessage(BaseModel):
    message: str
    target_segment: str = "all"  # all, regular, premium, occasional
    language: str = "hi"

class LoyaltyPointsUpdate(BaseModel):
    points: int
    reason: str

@router.get("/customers")
async def get_customers(
    customer_type: Optional[str] = None,
    active_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all customers for the business"""
    
    query = db.query(Customer).filter(Customer.business_owner_id == current_user.id)
    
    if customer_type:
        query = query.filter(Customer.customer_type == customer_type)
    
    if active_only:
        # Active customers are those who made a purchase in last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        query = query.filter(Customer.last_purchase_date >= thirty_days_ago)
    
    customers = query.all()
    
    return {
        "customers": [
            {
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "email": customer.email,
                "whatsapp_number": customer.whatsapp_number,
                "address": customer.address,
                "customer_type": customer.customer_type,
                "total_purchases": customer.total_purchases,
                "last_purchase_date": customer.last_purchase_date,
                "loyalty_points": customer.loyalty_points,
                "engagement_score": customer.engagement_score,
                "created_at": customer.created_at
            }
            for customer in customers
        ],
        "total_customers": len(customers),
        "segments": {
            "regular": len([c for c in customers if c.customer_type == "regular"]),
            "premium": len([c for c in customers if c.customer_type == "premium"]),
            "occasional": len([c for c in customers if c.customer_type == "occasional"])
        }
    }

@router.post("/customers")
async def create_customer(
    customer_data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new customer"""
    
    # Check if customer already exists with same phone
    existing_customer = db.query(Customer).filter(
        Customer.business_owner_id == current_user.id,
        Customer.phone == customer_data.phone
    ).first()
    
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this phone number already exists"
        )
    
    # Create new customer
    new_customer = Customer(
        name=customer_data.name,
        phone=customer_data.phone,
        email=customer_data.email,
        whatsapp_number=customer_data.whatsapp_number,
        address=customer_data.address,
        customer_type=customer_data.customer_type,
        business_owner_id=current_user.id
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return {
        "message": "Customer created successfully",
        "customer": {
            "id": new_customer.id,
            "name": new_customer.name,
            "phone": new_customer.phone,
            "customer_type": new_customer.customer_type
        }
    }

@router.put("/customers/{customer_id}")
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update customer information"""
    
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.business_owner_id == current_user.id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Update fields
    for field, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    
    customer.updated_at = datetime.now()
    db.commit()
    db.refresh(customer)
    
    return {
        "message": "Customer updated successfully",
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "customer_type": customer.customer_type
        }
    }

@router.delete("/customers/{customer_id}")
async def delete_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a customer"""
    
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.business_owner_id == current_user.id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    db.delete(customer)
    db.commit()
    
    return {"message": "Customer deleted successfully"}

@router.put("/customers/{customer_id}/loyalty")
async def update_loyalty_points(
    customer_id: int,
    loyalty_data: LoyaltyPointsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add or subtract loyalty points for a customer"""
    
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.business_owner_id == current_user.id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Update loyalty points
    customer.loyalty_points += loyalty_data.points
    if customer.loyalty_points < 0:
        customer.loyalty_points = 0
    
    customer.updated_at = datetime.now()
    db.commit()
    db.refresh(customer)
    
    return {
        "message": f"Loyalty points updated: {loyalty_data.points} points {loyalty_data.reason}",
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "loyalty_points": customer.loyalty_points,
            "points_change": loyalty_data.points,
            "reason": loyalty_data.reason
        }
    }

@router.post("/promotions/send")
async def send_promotion_message(
    promotion_data: PromotionMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send promotion message to customers"""
    
    # Get target customers based on segment
    query = db.query(Customer).filter(Customer.business_owner_id == current_user.id)
    
    if promotion_data.target_segment != "all":
        query = query.filter(Customer.customer_type == promotion_data.target_segment)
    
    target_customers = query.all()
    
    if not target_customers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No customers found in the target segment"
        )
    
    # In a real implementation, this would integrate with WhatsApp Business API
    # For now, we'll simulate the process
    
    successful_sends = 0
    failed_sends = 0
    
    for customer in target_customers:
        if customer.whatsapp_number:
            # Simulate successful send
            successful_sends += 1
        else:
            failed_sends += 1
    
    return {
        "message": "Promotion sent successfully",
        "details": {
            "promotion_text": promotion_data.message,
            "target_segment": promotion_data.target_segment,
            "language": promotion_data.language,
            "total_customers": len(target_customers),
            "successful_sends": successful_sends,
            "failed_sends": failed_sends
        }
    }

@router.get("/analytics")
async def get_customer_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get customer analytics and insights"""
    
    customers = db.query(Customer).filter(Customer.business_owner_id == current_user.id).all()
    
    if not customers:
        return {
            "analytics": {
                "total_customers": 0,
                "customer_segments": {},
                "engagement_metrics": {},
                "loyalty_metrics": {}
            }
        }
    
    # Calculate analytics
    total_customers = len(customers)
    total_purchase_value = sum(c.total_purchases for c in customers)
    avg_purchase_value = total_purchase_value / total_customers if total_customers > 0 else 0
    
    # Customer segments
    segments = {}
    for customer_type in ["regular", "premium", "occasional"]:
        segment_customers = [c for c in customers if c.customer_type == customer_type]
        segments[customer_type] = {
            "count": len(segment_customers),
            "percentage": (len(segment_customers) / total_customers) * 100 if total_customers > 0 else 0,
            "avg_purchase_value": sum(c.total_purchases for c in segment_customers) / len(segment_customers) if segment_customers else 0
        }
    
    # Engagement metrics
    thirty_days_ago = datetime.now() - timedelta(days=30)
    active_customers = [c for c in customers if c.last_purchase_date and c.last_purchase_date >= thirty_days_ago]
    
    engagement_metrics = {
        "active_customers": len(active_customers),
        "inactive_customers": total_customers - len(active_customers),
        "avg_engagement_score": sum(c.engagement_score or 0 for c in customers) / total_customers,
        "customers_with_whatsapp": len([c for c in customers if c.whatsapp_number])
    }
    
    # Loyalty metrics
    loyalty_metrics = {
        "total_points_issued": sum(c.loyalty_points for c in customers),
        "customers_with_points": len([c for c in customers if c.loyalty_points > 0]),
        "avg_points_per_customer": sum(c.loyalty_points for c in customers) / total_customers
    }
    
    # Top customers
    top_customers = sorted(customers, key=lambda x: x.total_purchases, reverse=True)[:5]
    
    return {
        "analytics": {
            "total_customers": total_customers,
            "total_purchase_value": total_purchase_value,
            "avg_purchase_value": avg_purchase_value,
            "customer_segments": segments,
            "engagement_metrics": engagement_metrics,
            "loyalty_metrics": loyalty_metrics,
            "top_customers": [
                {
                    "name": customer.name,
                    "total_purchases": customer.total_purchases,
                    "loyalty_points": customer.loyalty_points,
                    "customer_type": customer.customer_type
                }
                for customer in top_customers
            ]
        }
    }

@router.get("/segments")
async def get_customer_segments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get customer segmentation information"""
    
    return {
        "segments": {
            "regular": {
                "description": "Customers who visit regularly and make consistent purchases",
                "criteria": "5+ purchases, ₹1000+ total value",
                "benefits": "Standard loyalty points, regular promotions"
            },
            "premium": {
                "description": "High-value customers with significant purchase history",
                "criteria": "10+ purchases, ₹5000+ total value",
                "benefits": "Exclusive offers, priority service, bonus points"
            },
            "occasional": {
                "description": "Customers who visit infrequently",
                "criteria": "Less than 3 purchases, under ₹500 total value",
                "benefits": "Welcome offers, retention campaigns"
            }
        },
        "recommended_actions": {
            "regular": [
                "Send weekly promotional messages",
                "Offer loyalty rewards for continued purchases",
                "Introduce them to new products"
            ],
            "premium": [
                "Provide exclusive early access to new products",
                "Offer personalized recommendations",
                "Create VIP experiences"
            ],
            "occasional": [
                "Send comeback offers and discounts",
                "Remind them of products they previously bought",
                "Encourage more frequent visits"
            ]
        }
    }