from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import models, database  
from security import hashing        
import schemas
from typing import List
from security import Oauth2

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pwd = hashing.Hash.pbkdf2_sha256(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        role=models.UserRole.BUYER
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user


@router.get("/", response_model=List[schemas.UserOut])
def show_all_users(db: Session = Depends(database.get_db), current_user: models.User = Depends(Oauth2.get_admin_user)):
    
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=schemas.UserOut)  
def show_user(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(Oauth2.get_admin_user)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{id}", response_model=schemas.UserOut)
def delete_user(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(Oauth2.get_admin_user)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return user


@router.post("/apply_seller", status_code=status.HTTP_200_OK)
def apply_for_seller(db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_current_user)):
    
    if current_user.role == models.UserRole.SELLER:
        return {"message": "You are already a Seller!"}

    if current_user.seller_request_status == models.SellerStatus.PENDING:
        return {"message": "Your application is already pending."}

    current_user.seller_request_status = models.SellerStatus.PENDING

    db.commit()
    return {"message": "Application submitted successfully. Waiting for Admin approval."}



@router.put("/approve_seller/{user_id}", status_code=status.HTTP_200_OK)
def approve_seller(user_id: int, db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_admin_user)):
    
    user_to_promote = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user_to_promote: 
        raise HTTPException(status_code=404, detail="User not found")

    user_to_promote.role = models.UserRole.SELLER
    user_to_promote.seller_request_status = models.SellerStatus.NONE # Reset status
    
    db.commit()
    return {"message": f"User {user_to_promote.username} has been promoted to SELLER."}