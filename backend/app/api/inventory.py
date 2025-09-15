from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.database import get_db
from app.models.schemas import User, InventoryItem
from app.api.auth import get_current_user

router = APIRouter()

class InventoryItemCreate(BaseModel):
    name: str
    category: str
    sku: str
    current_stock: int
    min_stock_level: int = 10
    max_stock_level: int = 100
    unit_price: float
    cost_price: float
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_perishable: bool = False

class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    current_stock: Optional[int] = None
    min_stock_level: Optional[int] = None
    max_stock_level: Optional[int] = None
    unit_price: Optional[float] = None
    cost_price: Optional[float] = None
    supplier_name: Optional[str] = None
    supplier_contact: Optional[str] = None
    expiry_date: Optional[datetime] = None
    is_perishable: Optional[bool] = None

class StockUpdate(BaseModel):
    quantity: int
    operation: str  # "add" or "subtract"
    reason: Optional[str] = None

@router.get("/items")
async def get_inventory_items(
    category: Optional[str] = None,
    low_stock_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all inventory items for the user"""
    
    query = db.query(InventoryItem).filter(InventoryItem.owner_id == current_user.id)
    
    if category:
        query = query.filter(InventoryItem.category == category)
    
    if low_stock_only:
        query = query.filter(InventoryItem.current_stock <= InventoryItem.min_stock_level)
    
    items = query.all()
    
    return {
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "sku": item.sku,
                "current_stock": item.current_stock,
                "min_stock_level": item.min_stock_level,
                "max_stock_level": item.max_stock_level,
                "unit_price": item.unit_price,
                "cost_price": item.cost_price,
                "supplier_name": item.supplier_name,
                "supplier_contact": item.supplier_contact,
                "expiry_date": item.expiry_date,
                "is_perishable": item.is_perishable,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            }
            for item in items
        ],
        "total_items": len(items),
        "low_stock_items": len([item for item in items if item.current_stock <= item.min_stock_level])
    }

@router.post("/items")
async def create_inventory_item(
    item_data: InventoryItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new inventory item"""
    
    # Check if SKU already exists for this user
    existing_item = db.query(InventoryItem).filter(
        InventoryItem.owner_id == current_user.id,
        InventoryItem.sku == item_data.sku
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item with this SKU already exists"
        )
    
    # Create new inventory item
    new_item = InventoryItem(
        name=item_data.name,
        category=item_data.category,
        sku=item_data.sku,
        current_stock=item_data.current_stock,
        min_stock_level=item_data.min_stock_level,
        max_stock_level=item_data.max_stock_level,
        unit_price=item_data.unit_price,
        cost_price=item_data.cost_price,
        supplier_name=item_data.supplier_name,
        supplier_contact=item_data.supplier_contact,
        expiry_date=item_data.expiry_date,
        is_perishable=item_data.is_perishable,
        owner_id=current_user.id
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
        "message": "Inventory item created successfully",
        "item": {
            "id": new_item.id,
            "name": new_item.name,
            "category": new_item.category,
            "sku": new_item.sku,
            "current_stock": new_item.current_stock,
            "unit_price": new_item.unit_price
        }
    }

@router.put("/items/{item_id}")
async def update_inventory_item(
    item_id: int,
    item_data: InventoryItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an inventory item"""
    
    item = db.query(InventoryItem).filter(
        InventoryItem.id == item_id,
        InventoryItem.owner_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    # Update fields
    for field, value in item_data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    
    item.updated_at = datetime.now()
    db.commit()
    db.refresh(item)
    
    return {
        "message": "Inventory item updated successfully",
        "item": {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "current_stock": item.current_stock,
            "unit_price": item.unit_price
        }
    }

@router.delete("/items/{item_id}")
async def delete_inventory_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an inventory item"""
    
    item = db.query(InventoryItem).filter(
        InventoryItem.id == item_id,
        InventoryItem.owner_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "Inventory item deleted successfully"}

@router.put("/items/{item_id}/stock")
async def update_stock(
    item_id: int,
    stock_data: StockUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update stock quantity for an item"""
    
    item = db.query(InventoryItem).filter(
        InventoryItem.id == item_id,
        InventoryItem.owner_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    # Update stock based on operation
    if stock_data.operation == "add":
        item.current_stock += stock_data.quantity
    elif stock_data.operation == "subtract":
        if item.current_stock < stock_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock for this operation"
            )
        item.current_stock -= stock_data.quantity
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid operation. Use 'add' or 'subtract'"
        )
    
    item.updated_at = datetime.now()
    db.commit()
    db.refresh(item)
    
    return {
        "message": f"Stock {stock_data.operation}ed successfully",
        "item": {
            "id": item.id,
            "name": item.name,
            "current_stock": item.current_stock,
            "operation": stock_data.operation,
            "quantity": stock_data.quantity
        }
    }

@router.get("/alerts")
async def get_inventory_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get inventory alerts (low stock, expiring items, etc.)"""
    
    items = db.query(InventoryItem).filter(InventoryItem.owner_id == current_user.id).all()
    
    alerts = {
        "low_stock": [],
        "out_of_stock": [],
        "expiring_soon": [],
        "expired": []
    }
    
    for item in items:
        # Low stock alert
        if item.current_stock <= item.min_stock_level and item.current_stock > 0:
            alerts["low_stock"].append({
                "id": item.id,
                "name": item.name,
                "current_stock": item.current_stock,
                "min_stock_level": item.min_stock_level
            })
        
        # Out of stock alert
        if item.current_stock == 0:
            alerts["out_of_stock"].append({
                "id": item.id,
                "name": item.name,
                "supplier_name": item.supplier_name,
                "supplier_contact": item.supplier_contact
            })
        
        # Expiry alerts
        if item.expiry_date:
            days_to_expiry = (item.expiry_date - datetime.now()).days
            
            if days_to_expiry < 0:
                alerts["expired"].append({
                    "id": item.id,
                    "name": item.name,
                    "expiry_date": item.expiry_date,
                    "days_expired": abs(days_to_expiry)
                })
            elif days_to_expiry <= 7:
                alerts["expiring_soon"].append({
                    "id": item.id,
                    "name": item.name,
                    "expiry_date": item.expiry_date,
                    "days_remaining": days_to_expiry
                })
    
    return {
        "alerts": alerts,
        "summary": {
            "total_alerts": sum(len(alert_list) for alert_list in alerts.values()),
            "low_stock_count": len(alerts["low_stock"]),
            "out_of_stock_count": len(alerts["out_of_stock"]),
            "expiring_soon_count": len(alerts["expiring_soon"]),
            "expired_count": len(alerts["expired"])
        }
    }

@router.get("/categories")
async def get_inventory_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all unique categories for user's inventory"""
    
    categories = db.query(InventoryItem.category).filter(
        InventoryItem.owner_id == current_user.id
    ).distinct().all()
    
    category_list = [cat[0] for cat in categories if cat[0]]
    
    return {
        "categories": category_list,
        "total_categories": len(category_list)
    }

@router.get("/summary")
async def get_inventory_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get inventory summary statistics"""
    
    items = db.query(InventoryItem).filter(InventoryItem.owner_id == current_user.id).all()
    
    if not items:
        return {
            "summary": {
                "total_items": 0,
                "total_stock_value": 0,
                "low_stock_items": 0,
                "categories": 0
            }
        }
    
    total_stock_value = sum(item.current_stock * item.unit_price for item in items)
    low_stock_items = len([item for item in items if item.current_stock <= item.min_stock_level])
    unique_categories = len(set(item.category for item in items if item.category))
    
    return {
        "summary": {
            "total_items": len(items),
            "total_stock_value": total_stock_value,
            "low_stock_items": low_stock_items,
            "categories": unique_categories
        },
        "top_items_by_value": [
            {
                "name": item.name,
                "category": item.category,
                "stock_value": item.current_stock * item.unit_price
            }
            for item in sorted(items, key=lambda x: x.current_stock * x.unit_price, reverse=True)[:5]
        ]
    }