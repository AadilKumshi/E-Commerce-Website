from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List
import enum


# This prevents us from re-typing username/email over and over
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserOverview(UserBase):
    role: str
    class Config:
        from_attributes = True

# Registration
class UserCreate(UserBase):
    password: str


 # We return the ID and Role so the frontend knows who they are.
class UserOut(UserBase):
    id: int
    is_active: bool
    role: str
    seller_request_status: str

    class Config:
        from_attributes = True  # Necessary for Pydantic to read SQLAlchemy models


# 4. Login (Input)
class Login(BaseModel):
    username: str
    password: str


# This is what we return when they log in successfully
class Token(BaseModel):
    access_token: str
    token_type: str


# Used to validate the data inside the token
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = None  # <-- New Field

class ProductCreate(ProductBase):
    pass 

class ProductOut(ProductBase):
    id: int
    seller_id: int
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    product_id: int
    quantity: int


class BuyerInfo(BaseModel):
    username: str
    email: str
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    status: str
    date_created: datetime
    product_id: int
    quantity: int
    price_at_purchase: float
    buyer: BuyerInfo

    class Config:
        from_attributes = True


class OrderItemSeller(BaseModel):
    id: int               # Item ID
    order_id: int         
    product_id: int
    quantity: int
    price_at_purchase: float
    product: ProductOut   

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    product_id: int
    rating: int  
    text: str

class ReviewOut(BaseModel):
    id: int
    rating: int
    text: str

    sentiment_score: float
    sentiment_label: str

    user_id: int
    product_id: int
 
    class Config:
        from_attributes = True

class OrderStatusEnum(str, enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum