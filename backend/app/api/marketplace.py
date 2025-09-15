from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import requests
import json

from app.models.database import get_db
from app.models.schemas import User, InventoryItem, MarketplaceListing
from app.api.auth import get_current_user

router = APIRouter()

class MarketplaceListingCreate(BaseModel):
    inventory_item_id: int
    marketplace: str  # ondc, flipkart, amazon, meesho
    listing_title: str
    listing_description: str
    listing_price: float

class MarketplaceListingUpdate(BaseModel):
    listing_title: Optional[str] = None
    listing_description: Optional[str] = None
    listing_price: Optional[float] = None
    listing_status: Optional[str] = None

class ProductOptimizationRequest(BaseModel):
    product_name: str
    category: str
    description: str
    target_marketplace: str

@router.get("/supported-marketplaces")
async def get_supported_marketplaces():
    """Get list of supported marketplaces"""
    
    return {
        "marketplaces": [
            {
                "id": "ondc",
                "name": "ONDC (Open Network for Digital Commerce)",
                "description": "Government of India's unified platform for digital commerce",
                "commission_rate": "3-5%",
                "setup_difficulty": "Medium",
                "features": ["No commission on platform fee", "Government backing", "Interoperable network"],
                "supported": True
            },
            {
                "id": "flipkart",
                "name": "Flipkart",
                "description": "India's leading e-commerce marketplace",
                "commission_rate": "5-20%",
                "setup_difficulty": "Medium",
                "features": ["Large customer base", "Seller support", "Logistics support"],
                "supported": True
            },
            {
                "id": "amazon",
                "name": "Amazon India",
                "description": "Global e-commerce giant with strong India presence",
                "commission_rate": "5-15%",
                "setup_difficulty": "Medium",
                "features": ["Prime delivery", "FBA support", "Global reach"],
                "supported": True
            },
            {
                "id": "meesho",
                "name": "Meesho",
                "description": "Social commerce platform for small businesses",
                "commission_rate": "0-5%",
                "setup_difficulty": "Easy",
                "features": ["Zero commission", "Reseller network", "Easy setup"],
                "supported": True
            }
        ],
        "integration_status": {
            "ondc": "Beta",
            "flipkart": "Available",
            "amazon": "Available", 
            "meesho": "Available"
        }
    }

@router.get("/listings")
async def get_marketplace_listings(
    marketplace: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's marketplace listings"""
    
    query = db.query(MarketplaceListing).join(InventoryItem).filter(
        InventoryItem.owner_id == current_user.id
    )
    
    if marketplace:
        query = query.filter(MarketplaceListing.marketplace == marketplace)
    
    if status_filter:
        query = query.filter(MarketplaceListing.listing_status == status_filter)
    
    listings = query.all()
    
    return {
        "listings": [
            {
                "id": listing.id,
                "inventory_item_id": listing.inventory_item_id,
                "marketplace": listing.marketplace,
                "listing_id": listing.listing_id,
                "listing_title": listing.listing_title,
                "listing_description": listing.listing_description,
                "listing_price": listing.listing_price,
                "listing_status": listing.listing_status,
                "ai_optimized": listing.ai_optimized,
                "performance_metrics": listing.performance_metrics,
                "created_at": listing.created_at,
                "updated_at": listing.updated_at
            }
            for listing in listings
        ],
        "total_listings": len(listings),
        "marketplace_breakdown": {
            marketplace: len([l for l in listings if l.marketplace == marketplace])
            for marketplace in ["ondc", "flipkart", "amazon", "meesho"]
        }
    }

@router.post("/listings")
async def create_marketplace_listing(
    listing_data: MarketplaceListingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new marketplace listing"""
    
    # Verify inventory item belongs to user
    inventory_item = db.query(InventoryItem).filter(
        InventoryItem.id == listing_data.inventory_item_id,
        InventoryItem.owner_id == current_user.id
    ).first()
    
    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    # Check if listing already exists for this item on this marketplace
    existing_listing = db.query(MarketplaceListing).filter(
        MarketplaceListing.inventory_item_id == listing_data.inventory_item_id,
        MarketplaceListing.marketplace == listing_data.marketplace
    ).first()
    
    if existing_listing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item already listed on {listing_data.marketplace}"
        )
    
    # Create marketplace listing
    new_listing = MarketplaceListing(
        inventory_item_id=listing_data.inventory_item_id,
        marketplace=listing_data.marketplace,
        listing_id=f"{listing_data.marketplace}_{inventory_item.sku}_{current_user.id}",
        listing_title=listing_data.listing_title,
        listing_description=listing_data.listing_description,
        listing_price=listing_data.listing_price,
        listing_status="pending",
        ai_optimized=False
    )
    
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    
    # In a real implementation, this would make API calls to the actual marketplace
    # For now, we'll simulate the listing process
    try:
        success = await _simulate_marketplace_listing(listing_data.marketplace, new_listing)
        if success:
            new_listing.listing_status = "active"
            db.commit()
    except Exception as e:
        new_listing.listing_status = "failed"
        db.commit()
    
    return {
        "message": "Marketplace listing created successfully",
        "listing": {
            "id": new_listing.id,
            "marketplace": new_listing.marketplace,
            "listing_id": new_listing.listing_id,
            "listing_title": new_listing.listing_title,
            "listing_status": new_listing.listing_status
        }
    }

@router.put("/listings/{listing_id}")
async def update_marketplace_listing(
    listing_id: int,
    listing_data: MarketplaceListingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a marketplace listing"""
    
    # Find listing and verify ownership
    listing = db.query(MarketplaceListing).join(InventoryItem).filter(
        MarketplaceListing.id == listing_id,
        InventoryItem.owner_id == current_user.id
    ).first()
    
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marketplace listing not found"
        )
    
    # Update fields
    for field, value in listing_data.dict(exclude_unset=True).items():
        setattr(listing, field, value)
    
    db.commit()
    db.refresh(listing)
    
    return {
        "message": "Marketplace listing updated successfully",
        "listing": {
            "id": listing.id,
            "marketplace": listing.marketplace,
            "listing_title": listing.listing_title,
            "listing_price": listing.listing_price,
            "listing_status": listing.listing_status
        }
    }

@router.delete("/listings/{listing_id}")
async def delete_marketplace_listing(
    listing_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a marketplace listing"""
    
    # Find listing and verify ownership
    listing = db.query(MarketplaceListing).join(InventoryItem).filter(
        MarketplaceListing.id == listing_id,
        InventoryItem.owner_id == current_user.id
    ).first()
    
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marketplace listing not found"
        )
    
    # In real implementation, would call marketplace API to delete listing
    db.delete(listing)
    db.commit()
    
    return {"message": "Marketplace listing deleted successfully"}

@router.post("/optimize-listing")
async def optimize_product_listing(
    request: ProductOptimizationRequest,
    current_user: User = Depends(get_current_user)
):
    """Use AI to optimize product listing for specific marketplace"""
    
    try:
        # Generate optimized listing using AI
        optimized_listing = await _generate_ai_optimized_listing(
            request.product_name,
            request.category,
            request.description,
            request.target_marketplace
        )
        
        return {
            "success": True,
            "original": {
                "product_name": request.product_name,
                "category": request.category,
                "description": request.description,
                "target_marketplace": request.target_marketplace
            },
            "optimized": optimized_listing,
            "improvements": [
                "SEO-optimized title with relevant keywords",
                "Enhanced description with bullet points",
                "Marketplace-specific formatting",
                "Competitive pricing suggestions",
                "Relevant tags and categories"
            ],
            "message": "Product listing optimized successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to optimize listing: {str(e)}"
        )

@router.get("/analytics")
async def get_marketplace_analytics(
    marketplace: Optional[str] = None,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get marketplace performance analytics"""
    
    query = db.query(MarketplaceListing).join(InventoryItem).filter(
        InventoryItem.owner_id == current_user.id
    )
    
    if marketplace:
        query = query.filter(MarketplaceListing.marketplace == marketplace)
    
    listings = query.all()
    
    if not listings:
        return {
            "analytics": {
                "total_listings": 0,
                "active_listings": 0,
                "marketplace_performance": {},
                "top_performing_products": []
            }
        }
    
    # Calculate analytics
    total_listings = len(listings)
    active_listings = len([l for l in listings if l.listing_status == "active"])
    
    # Marketplace performance breakdown
    marketplace_performance = {}
    for marketplace_name in ["ondc", "flipkart", "amazon", "meesho"]:
        marketplace_listings = [l for l in listings if l.marketplace == marketplace_name]
        marketplace_performance[marketplace_name] = {
            "total_listings": len(marketplace_listings),
            "active_listings": len([l for l in marketplace_listings if l.listing_status == "active"]),
            "avg_price": sum(l.listing_price for l in marketplace_listings) / len(marketplace_listings) if marketplace_listings else 0
        }
    
    # Simulated performance metrics (in real implementation, would come from marketplace APIs)
    top_performing_products = [
        {
            "listing_title": listing.listing_title,
            "marketplace": listing.marketplace,
            "listing_price": listing.listing_price,
            "views": 150,  # Simulated
            "orders": 5,   # Simulated
            "conversion_rate": 3.3  # Simulated
        }
        for listing in listings[:5]
    ]
    
    return {
        "analytics": {
            "period": f"Last {days} days",
            "total_listings": total_listings,
            "active_listings": active_listings,
            "marketplace_performance": marketplace_performance,
            "top_performing_products": top_performing_products,
            "insights": [
                "ONDC has the lowest commission rates",
                "Meesho is best for social commerce",
                "Amazon has highest conversion rates",
                "Flipkart has largest reach in India"
            ]
        }
    }

@router.post("/bulk-list")
async def bulk_list_products(
    marketplace: str,
    inventory_item_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Bulk list multiple products on a marketplace"""
    
    if marketplace not in ["ondc", "flipkart", "amazon", "meesho"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported marketplace"
        )
    
    # Verify all inventory items belong to user
    inventory_items = db.query(InventoryItem).filter(
        InventoryItem.id.in_(inventory_item_ids),
        InventoryItem.owner_id == current_user.id
    ).all()
    
    if len(inventory_items) != len(inventory_item_ids):
        raise HTTPException(
            status_code=404,
            detail="Some inventory items not found"
        )
    
    results = []
    
    for item in inventory_items:
        try:
            # Check if already listed
            existing_listing = db.query(MarketplaceListing).filter(
                MarketplaceListing.inventory_item_id == item.id,
                MarketplaceListing.marketplace == marketplace
            ).first()
            
            if existing_listing:
                results.append({
                    "item_id": item.id,
                    "item_name": item.name,
                    "status": "skipped",
                    "reason": "Already listed on this marketplace"
                })
                continue
            
            # Generate AI-optimized listing
            optimized = await _generate_ai_optimized_listing(
                item.name,
                item.category,
                f"High-quality {item.name} at competitive price",
                marketplace
            )
            
            # Create listing
            new_listing = MarketplaceListing(
                inventory_item_id=item.id,
                marketplace=marketplace,
                listing_id=f"{marketplace}_{item.sku}_{current_user.id}",
                listing_title=optimized["title"],
                listing_description=optimized["description"],
                listing_price=item.unit_price,
                listing_status="active",
                ai_optimized=True
            )
            
            db.add(new_listing)
            
            results.append({
                "item_id": item.id,
                "item_name": item.name,
                "status": "success",
                "listing_id": new_listing.listing_id
            })
            
        except Exception as e:
            results.append({
                "item_id": item.id,
                "item_name": item.name,
                "status": "failed",
                "reason": str(e)
            })
    
    db.commit()
    
    success_count = len([r for r in results if r["status"] == "success"])
    
    return {
        "message": f"Bulk listing completed: {success_count}/{len(inventory_item_ids)} items listed successfully",
        "marketplace": marketplace,
        "results": results,
        "summary": {
            "total_items": len(inventory_item_ids),
            "successful": success_count,
            "failed": len([r for r in results if r["status"] == "failed"]),
            "skipped": len([r for r in results if r["status"] == "skipped"])
        }
    }

async def _simulate_marketplace_listing(marketplace: str, listing: MarketplaceListing) -> bool:
    """Simulate marketplace listing process (replace with real API calls)"""
    
    # Simulate different success rates for different marketplaces
    success_rates = {
        "ondc": 0.95,
        "flipkart": 0.90,
        "amazon": 0.85,
        "meesho": 0.98
    }
    
    import random
    return random.random() < success_rates.get(marketplace, 0.9)

async def _generate_ai_optimized_listing(
    product_name: str, 
    category: str, 
    description: str, 
    marketplace: str
) -> Dict[str, Any]:
    """Generate AI-optimized product listing"""
    
    # Marketplace-specific optimization rules
    marketplace_rules = {
        "ondc": {
            "title_format": "{product_name} - High Quality {category} | Best Price",
            "description_focus": "Quality and value proposition",
            "keywords": ["authentic", "genuine", "best price", "quality"]
        },
        "flipkart": {
            "title_format": "{product_name} | {category} | Fast Delivery",
            "description_focus": "Features and benefits",
            "keywords": ["bestseller", "trending", "fast delivery", "customer choice"]
        },
        "amazon": {
            "title_format": "{product_name} - Premium {category} with Fast Shipping",
            "description_focus": "Premium positioning",
            "keywords": ["premium", "amazon's choice", "fast shipping", "top rated"]
        },
        "meesho": {
            "title_format": "{product_name} | Wholesale Price | {category}",
            "description_focus": "Affordability and bulk benefits",
            "keywords": ["wholesale", "bulk discount", "reseller friendly", "low price"]
        }
    }
    
    rules = marketplace_rules.get(marketplace, marketplace_rules["flipkart"])
    
    # Generate optimized title
    optimized_title = rules["title_format"].format(
        product_name=product_name,
        category=category
    )
    
    # Generate optimized description
    optimized_description = f"""
🌟 {product_name} - Premium Quality {category}

✅ Key Features:
• High-quality materials and construction
• Competitive pricing with best value
• Fast and reliable delivery
• Customer satisfaction guaranteed

📦 Product Details:
{description}

🚚 Delivery: Fast shipping available
💰 Price: Best market rates
⭐ Quality: Premium grade guarantee

{' '.join(['#' + keyword for keyword in rules['keywords']])}
    """.strip()
    
    return {
        "title": optimized_title,
        "description": optimized_description,
        "suggested_tags": rules["keywords"],
        "pricing_strategy": "competitive",
        "marketplace_specific_tips": [
            f"Optimized for {marketplace} algorithm",
            "SEO-friendly title with relevant keywords",
            "Clear value proposition highlighted",
            "Professional formatting for better conversion"
        ]
    }