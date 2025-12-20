from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import security.JWT as JWT
import database.database as database
import database.models as models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_username = JWT.verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.username == token_username).first()
    
    if user is None:
        raise credentials_exception
        
    return user

# Admin Only
def get_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have Admin privileges"
        )
    return current_user

# Seller or Admin
def get_seller_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role not in [models.UserRole.SELLER, models.UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You must be a Seller to perform this action"
        )
    return current_user