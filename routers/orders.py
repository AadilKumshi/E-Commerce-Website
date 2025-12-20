from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import models, database  
from security import  Oauth2       
import schemas
from typing import List


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.OrderOut)
def create_order(order_details: schemas.OrderCreate, db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_current_user)):
    
    product = db.query(models.Product).filter(models.Product.id == order_details.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < order_details.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    if product.seller_id == current_user.id:
        raise HTTPException(status_code=403, detail="You cannot purchase your own product")

    new_order = models.Order(
        buyer_id=current_user.id,
        product_id=product.id,      # Direct Link
        quantity=order_details.quantity,
        price_at_purchase=product.price,        # Snapshot
        status=models.OrderStatus.PENDING
    )
    db.add(new_order)

    product.stock = product.stock - order_details.quantity
    
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/seller_dashboard", response_model=List[schemas.OrderOut]) # Use OrderOut
def get_seller_orders(db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_seller_user)):
    
    orders = (
        db.query(models.Order)
        .join(models.Product)
        .filter(models.Product.seller_id == current_user.id)
        .all()
    )
    return orders
    

@router.put("/{order_id}/status", response_model=schemas.OrderOut)
def update_order_status(order_id: int,status_update: schemas.OrderStatusUpdate,db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_seller_user)):
    
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if status_update.status == schemas.OrderStatusEnum.CANCELLED:
        if order.status != schemas.OrderStatusEnum.CANCELLED:
            order.product.stock += order.quantity

    if order.product.seller_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You are not authorized to manage this order. It does not contain your product."
        )

    order.status = status_update.status 
    
    db.commit()
    db.refresh(order)
    return order