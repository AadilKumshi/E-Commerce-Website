from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import models, database  
from security import  Oauth2       
import schemas
from typing import List, Optional
from sqlalchemy import or_, desc
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(Oauth2.get_seller_user)):
    
    new_product = models.Product(
        **product.dict(),
        seller_id=current_user.id 
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_seller_user)):
    
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if not (product.seller_id == current_user.id or current_user.role == models.UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You are not authorized to delete this product"
        )

    product_query.delete(synchronize_session=False)
    db.commit()
    return


# In routers/products.py

@router.get("/", response_model=List[schemas.ProductOut]) # Ensure this matches your list schema
def get_products(
    db: Session = Depends(database.get_db),
    limit: int = 10,       
    skip: int = 0,
    sort: Optional[str] = "asc",         
    search: Optional[str] = "" 
):

    products_query = db.query(models.Product)
    
    if search:
        products_query = products_query.filter(models.Product.name.contains(search))
    
    if sort == "asc":
        products_query = products_query.order_by(models.Product.price.asc())
    elif sort == "desc":
        products_query = products_query.order_by(models.Product.price.desc())
    else:
        products_query = products_query.order_by(models.Product.id.desc())

    products = products_query.offset(skip).limit(limit).all()
    return products


@router.get("/my_products", response_model=List[schemas.ProductOut])
def get_my_products(db: Session = Depends(database.get_db),current_user: models.User = Depends(Oauth2.get_seller_user)):
    
    products = db.query(models.Product).filter(models.Product.seller_id == current_user.id).all()
    return products


@router.get("/{id}", response_model=List[schemas.ProductOut])
def show_product_by_seller(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(Oauth2.get_current_user)):
    
    product = db.query(models.Product).filter(models.Product.seller_id == id).all()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{id}/recommendations", response_model=List[schemas.ProductOut])
def get_recommendations(id: int, db: Session = Depends(database.get_db)):
    
    orders = db.query(models.Order.buyer_id, models.Order.product_id).all()
    
    if not orders:
        return []

    df = pd.DataFrame(orders, columns=['user_id', 'product_id'])

    # Pivot Table: Rows = Users, Cols = Products
    # fill_value=0 means "User didn't buy this"
    user_item_matrix = df.pivot_table(index='user_id', columns='product_id', aggfunc='size', fill_value=0)

    # Validation: If this specific product has never been bought, we can't find similarities
    if id not in user_item_matrix.columns:
        return []

    # Transpose so Products are rows (we want to compare products, not users)
    item_item_matrix = user_item_matrix.T
    
    # Calculate Cosine Similarity
    # This creates a matrix where every product is compared to every other product
    similarity_matrix = cosine_similarity(item_item_matrix)
    
    # Convert back to readable DataFrame with Product IDs as index/columns
    similarity_df = pd.DataFrame(similarity_matrix, index=item_item_matrix.index, columns=item_item_matrix.index)

    # Get the column for the requested product ID
    # Sort descending (1.0 is best match)
    # .iloc[1:4] takes top 3 (Skipping index 0 because that's the product itself)
    top_product_ids = similarity_df[id].sort_values(ascending=False).iloc[1:4].index.tolist()

    # Fetch the full product details from the database
    recommended_products = db.query(models.Product).filter(models.Product.id.in_(top_product_ids)).all()

    return recommended_products