from sqlalchemy import Column, Integer, String, Boolean, Enum as SAEnum, DateTime
from database.database import Base
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Float, Text, ForeignKey
from datetime import datetime

class UserRole(enum.Enum):
    ADMIN = "admin"
    SELLER = "seller"
    BUYER = "buyer"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class SellerStatus(str, enum.Enum):
    NONE = "none"         
    PENDING = "pending"   
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SAEnum(UserRole), default=UserRole.BUYER)
    seller_request_status = Column(SAEnum(SellerStatus), default=SellerStatus.NONE)

    products = relationship("Product", back_populates="owner")
    orders = relationship("Order", back_populates="buyer")
    reviews = relationship("Review", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer, default=0) # Track inventory
    seller_id = Column(Integer, ForeignKey("users.id"))
    image_url = Column(String, nullable=True)
    
    owner = relationship("User", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    status = Column(SAEnum(OrderStatus), default=OrderStatus.PENDING)
    quantity = Column(Integer, default=1)
    price_at_purchase = Column(Float)

    buyer_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    buyer = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")



class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    rating = Column(Integer)
    sentiment_score = Column(Float, nullable=True) # AI Generated 
    sentiment_label = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")