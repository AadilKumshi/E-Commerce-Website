from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from textblob import TextBlob 
from database import database, models
import schemas
from security import Oauth2

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReviewOut)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_current_user)):

    existing_review = db.query(models.Review).filter(
        models.Review.user_id == current_user.id,
        models.Review.product_id == review.product_id,
    ).first()

    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")

    
    verified_purchase = db.query(models.Order).filter(
        models.Order.buyer_id == current_user.id,
        models.Order.product_id == review.product_id,
        models.Order.status == models.OrderStatus.DELIVERED 
    ).first()

    if not verified_purchase:
        raise HTTPException(
            status_code=403, 
            detail="You can only review products you have purchased."
        )

    blob = TextBlob(review.text)
    sentiment_score = blob.sentiment.polarity # -1 to 1

    if sentiment_score > 0.3:
        sentiment_label = "Positive"
    elif sentiment_score < -0.3:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    new_review = models.Review(
        user_id=current_user.id,
        product_id=review.product_id,
        rating=review.rating,
        text=review.text,
        sentiment_score=sentiment_score, 
        sentiment_label=sentiment_label 
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(Oauth2.get_current_user)):
    
    review_query = db.query(models.Review).filter(models.Review.id == id)
    review = review_query.first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    is_admin = current_user.role == models.UserRole.ADMIN 
    is_author = review.user_id == current_user.id

    if not is_admin and not is_author:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to delete this review"
        )

    db.delete(review)
    db.commit()

    return None

@router.get("/{product_id}", response_model=List[schemas.ReviewOut])
def get_reviews(product_id: int, db: Session = Depends(database.get_db), sentiment_label: Optional[str] = None):
    
    query = db.query(models.Review).filter(models.Review.product_id == product_id)

    if sentiment_label:
        query = query.filter(models.Review.sentiment_label == sentiment_label.capitalize())

    return query.all()