from fastapi import FastAPI
import database.models as models
from database.database import engine
import routers.authentication as authentication
from routers import users, products, orders, reviews

app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(reviews.router)



models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce API", "status": "active"}  
