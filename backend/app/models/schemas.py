from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base

class User(Base):
    """User model for shop owners and business users"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    business_name = Column(String)
    business_type = Column(String)  # kirana, restaurant, retail, etc.
    preferred_language = Column(String, default="hi")  # Hindi default
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="owner")
    customers = relationship("Customer", back_populates="business_owner")
    transactions = relationship("Transaction", back_populates="user")

class InventoryItem(Base):
    """Inventory items for businesses"""
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    current_stock = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=10)
    max_stock_level = Column(Integer, default=100)
    unit_price = Column(Float)
    cost_price = Column(Float)
    supplier_name = Column(String)
    supplier_contact = Column(String)
    expiry_date = Column(DateTime, nullable=True)
    is_perishable = Column(Boolean, default=False)
    seasonal_demand = Column(JSON)  # Store seasonal patterns
    festival_demand = Column(JSON)  # Store festival-specific demand
    ai_forecast = Column(JSON)  # AI predictions
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="inventory_items")

class Customer(Base):
    """Customer information and engagement data"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, index=True)
    email = Column(String, nullable=True)
    whatsapp_number = Column(String, nullable=True)
    address = Column(Text)
    customer_type = Column(String)  # regular, premium, occasional
    total_purchases = Column(Float, default=0.0)
    last_purchase_date = Column(DateTime, nullable=True)
    preferred_products = Column(JSON)  # AI-analyzed preferences
    engagement_score = Column(Float, default=0.0)
    loyalty_points = Column(Integer, default=0)
    business_owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business_owner = relationship("User", back_populates="customers")
    transactions = relationship("Transaction", back_populates="customer")

class Transaction(Base):
    """Sales and financial transactions"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String)  # sale, purchase, expense, refund
    amount = Column(Float)
    payment_method = Column(String)  # cash, upi, card
    upi_transaction_id = Column(String, nullable=True)
    description = Column(Text)
    items_sold = Column(JSON)  # List of items and quantities
    profit_margin = Column(Float, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="transactions")
    user = relationship("User", back_populates="transactions")

class AIInteraction(Base):
    """Log of AI agent interactions and decisions"""
    __tablename__ = "ai_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_type = Column(String)  # inventory, customer, finance
    interaction_type = Column(String)  # voice, text, auto
    input_data = Column(JSON)
    output_data = Column(JSON)
    confidence_score = Column(Float)
    language_used = Column(String)
    was_successful = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MarketplaceListing(Base):
    """Products listed on various marketplaces"""
    __tablename__ = "marketplace_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"))
    marketplace = Column(String)  # ondc, flipkart, amazon, meesho
    listing_id = Column(String)
    listing_title = Column(String)
    listing_description = Column(Text)
    listing_price = Column(Float)
    listing_status = Column(String)  # active, inactive, out_of_stock
    ai_optimized = Column(Boolean, default=False)
    performance_metrics = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())