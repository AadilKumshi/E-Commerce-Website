from sqlalchemy.orm import Session
from database import database, models


db = database.SessionLocal()

TARGET_USERNAME = "aadil" 
user = db.query(models.User).filter(models.User.username == TARGET_USERNAME).first()

if not user:
    print(f"User '{TARGET_USERNAME}' not found!")
else:
    user.role = models.UserRole.ADMIN
    db.commit()
    db.refresh(user)
    print(f"User '{user.username}' is now an ADMIN.")
    print(f"Current Role: {user.role}")

db.close()