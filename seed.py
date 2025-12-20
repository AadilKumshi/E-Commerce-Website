import random
from faker import Faker
from database.database import engine, SessionLocal
from database import models
from passlib.context import CryptContext
from textblob import TextBlob 


fake = Faker()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
HASHED_PASSWORD = pwd_context.hash("1234")


INDIAN_NAMES = [
    "Aarav Patel", "Vihaan Sharma", "Aditya Verma", "Sai Iyer", "Arjun Reddy",
    "Rohan Gupta", "Karthik Nair", "Vikram Singh", "Rahul Mehta", "Ishaan Malhotra",
    "Vivaan Joshi", "Dhruv Kapoor", "Kabir Das", "Reyansh Saxena", "Aryan Jain",
    "Siddharth Rao", "Kiara Shetty", "Ananya Mishra", "Diya Kaur", "Pari Chopra",
    "Saanvi Deshmukh", "Aadhya Pillai", "Myra Kulkarni", "Zara Khan", "Ishita Hegde",
    "Riya Solanki", "Anjali Dubey", "Kavya Gowda", "Neha Agarwal", "Pooja Bhat",
    "Amit Tiwari", "Sneha Roy", "Manish Pandey", "Varun Chawla", "Abhishek Sinha",
    "Priya Venkatesh", "Rajeshwari S", "Suresh Menon", "Deepak Kumar", "Meera Krishnan",
    "Nikhil Bansal", "Tanvi Choudhary", "Rishabh Goel", "Simran Dhillon", "Gaurav Sethi",
    "Pallavi Joshi", "Naveen Reddy", "Swati Bose", "Tarun Khatri", "Lata Mangeshkar", 
    "Kamal Hasan", "Sania Mirza", "Virat Kohli", "Mahendra Singh", "Rohit Sharma",
    "Hardik Pandya", "Ravindra Jadeja", "Jasprit Bumrah", "Shubman Gill", "KL Rahul"
]


SELLER_NAMES = ["Apple", "Samsung", "Microsoft", "Xiaomi", "OnePlus"]

PRODUCT_CATALOG = {
    "Apple": [
        "iPhone 15 Pro Max", "iPhone 15", "iPhone 14 Plus", "iPhone 13 Mini", 
        "MacBook Air M2", "MacBook Pro 14 M3", "MacBook Pro 16 M3 Max", "iMac 24-inch",
        "iPad Pro 12.9", "iPad Air 5th Gen", "iPad Mini 6", "iPad 10th Gen",
        "Apple Watch Ultra 2", "Apple Watch Series 9", "Apple Watch SE",
        "AirPods Pro 2nd Gen", "AirPods Max", "AirPods 3rd Gen",
        "Apple TV 4K", "HomePod Mini"
    ],
    "Samsung": [
        "Galaxy S24 Ultra", "Galaxy S24 Plus", "Galaxy Z Fold 5", "Galaxy Z Flip 5",
        "Galaxy Tab S9 Ultra", "Galaxy Tab S9 FE", "Galaxy Book 3 Ultra", "Galaxy Book 3 Pro",
        "Galaxy Watch 6 Classic", "Galaxy Watch 5 Pro", "Galaxy Fit 3",
        "Galaxy Buds 2 Pro", "Galaxy Buds FE", "Galaxy SmartTag2",
        "Samsung Odyssey G9 Monitor", "Smart Monitor M8", "990 Pro NVMe SSD 2TB",
        "T7 Shield Portable SSD", "Freestyle Gen 2 Projector", "Galaxy A54 5G"
    ],
    "Microsoft": [
        "Surface Pro 9", "Surface Pro 8", "Surface Laptop 5 15-inch", "Surface Laptop Studio 2",
        "Surface Go 3", "Surface Duo 2", "Surface Hub 2S",
        "Xbox Series X", "Xbox Series S", "Xbox Elite Controller Series 2",
        "Xbox Wireless Headset", "Surface Headphones 2", "Surface Earbuds",
        "Microsoft Ergonomic Keyboard", "Surface Arc Mouse", "Surface Pen",
        "Microsoft Modern Webcam", "Surface Dock 2", "Audio Dock", "HoloLens 2"
    ],
    "Xiaomi": [
        "Xiaomi 14 Ultra", "Xiaomi 13T Pro", "Redmi Note 13 Pro+", "POCO F5 Pro",
        "Xiaomi Pad 6", "Xiaomi Book S 12.4",
        "Xiaomi Smart Band 8", "Xiaomi Watch 2 Pro", "Redmi Watch 4",
        "Xiaomi Robot Vacuum X10", "Mi Air Purifier 4", "Xiaomi Electric Scooter 4 Ultra",
        "Mi Smart Air Fryer", "Mi TV Stick 4K", "Xiaomi Mesh System AX3000",
        "Redmi Buds 5 Pro", "Xiaomi 33W Power Bank", "Mi Bedside Lamp 2",
        "Mi Portable Photo Printer", "Xiaomi Electric Kettle 2"
    ],
    "OnePlus": [
        "OnePlus 12", "OnePlus 12R", "OnePlus Open", "OnePlus 11 5G",
        "OnePlus Nord 3", "OnePlus Nord CE 3 Lite",
        "OnePlus Pad", "OnePlus Pad Go",
        "OnePlus Watch 2", "OnePlus Band",
        "OnePlus Buds Pro 2", "OnePlus Buds 3", "OnePlus Nord Buds 2",
        "OnePlus Bullets Wireless Z2",
        "SUPERVOOC 100W Power Adapter", "OnePlus 80W Car Charger", "OnePlus AIRVOOC 50W",
        "OnePlus Keyboard 81 Pro", "OnePlus Monitor X 27", "OnePlus Gaming Triggers"
    ]
}


SHOPPING_PATTERNS = [
    ("Apple", ["iPhone 15 Pro Max", "AirPods Pro 2nd Gen", "Apple Watch Ultra 2"]),
    ("Apple", ["iPhone 15", "AirPods Pro 2nd Gen", "HomePod Mini"]),
    ("Apple", ["MacBook Air M2", "iPad Pro 12.9", "AirPods Pro 2nd Gen"]),
    ("Microsoft", ["Xbox Series X", "Xbox Elite Controller Series 2", "Smart Monitor M8"]),
    ("Microsoft", ["Xbox Series X", "Surface Headphones 2"]),
    ("Samsung", ["Galaxy S24 Ultra", "Galaxy Watch 6 Classic", "Galaxy Buds 2 Pro"]),
    ("Samsung", ["Galaxy Z Flip 5", "Galaxy Buds 2 Pro", "Galaxy Book 3 Pro"]),
    ("Xiaomi", ["Redmi Note 13 Pro+", "Xiaomi Smart Band 8", "Redmi Buds 5 Pro"]),
    ("Xiaomi", ["Xiaomi 14 Ultra", "Xiaomi Robot Vacuum X10"]),
    ("OnePlus", ["OnePlus 12", "OnePlus Buds Pro 2", "OnePlus Watch 2"]),
    ("OnePlus", ["OnePlus Open", "OnePlus Pad", "SUPERVOOC 100W Power Adapter"])
]

# Reviews
positive_texts = ["I absolutely love this product!", "Amazing quality.", "Five stars!", "Great value.", "Superb performance!"]
negative_texts = ["Terrible product.", "Arrived broken.", "Waste of money.", "Very disappointed.", "Not worth the price."]
neutral_texts = ["It is okay.", "Decent for the price.", "Nothing special.", "Average quality.", "Does the job."]

def get_review_data(vibe="positive"):
    if vibe == "positive": return random.choice(positive_texts), 5, "Positive"
    elif vibe == "negative": return random.choice(negative_texts), 1, "Negative"
    else: return random.choice(neutral_texts), 3, "Neutral"

def get_price(name):
    if "MacBook" in name or "Ultra" in name or "Fold" in name or "Pro" in name: return 1200.0
    if "iPhone" in name or "S24" in name or "Surface" in name or "14" in name: return 900.0
    if "Xbox" in name or "Pad" in name or "Monitor" in name: return 500.0
    return 150.0


def seed_data():
    print("Resetting Database...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        print("Creating Sellers...")
        seller_map = {} 
        for name in SELLER_NAMES:
            user = models.User(username=name.lower(), email=f"{name.lower()}@tech.com", hashed_password=HASHED_PASSWORD, role=models.UserRole.SELLER)
            session.add(user)
            seller_map[name] = user
        session.commit()

        print("Creating 100 Products...")
        product_map = {} 
        all_products_list = []
        
        for brand, items in PRODUCT_CATALOG.items():
            seller = seller_map[brand]
            session.refresh(seller)
            for item_name in items:
                prod = models.Product(
                    name=item_name, 
                    description=f"{brand} flagship product.", 
                    price=get_price(item_name), 
                    stock=100, 
                    seller_id=seller.id,
                    image_url=f"http://fake.com/{item_name.replace(' ', '_')}.jpg"
                )
                session.add(prod)
                product_map[item_name] = prod
                all_products_list.append(prod)
        session.commit()

        print("Executing Curated Order Patterns...")
        
        user_index = 0
        for _ in range(5): 
            for preferred_brand, shopping_cart in SHOPPING_PATTERNS:
                
                
                real_name = INDIAN_NAMES[user_index % len(INDIAN_NAMES)]
                username_slug = real_name.lower().replace(" ", "_")
                if user_index >= len(INDIAN_NAMES):
                    username_slug += f"_{user_index}"

                user = models.User(
                    username=username_slug,
                    email=f"{username_slug}@example.com",
                    hashed_password=HASHED_PASSWORD,
                    role=models.UserRole.BUYER
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                user_index += 1

                for item_name in shopping_cart:
                    product = product_map[item_name]
                    
                    order = models.Order(buyer_id=user.id, product_id=product.id, quantity=1, price_at_purchase=product.price, status=models.OrderStatus.DELIVERED)
                    session.add(order)
                    
                    vibe = random.choices(["positive", "negative", "neutral"], weights=[60, 30, 10], k=1)[0]
                    
                    text, rating, label = get_review_data(vibe)
                    blob = TextBlob(text)
                    review = models.Review(
                        user_id=user.id, product_id=product.id, text=text, rating=rating, sentiment_score=blob.sentiment.polarity, sentiment_label=label
                    )
                    session.add(review)

                if random.random() < 0.6: 
                    random_prod = random.choice(all_products_list)
                    order = models.Order(buyer_id=user.id, product_id=random_prod.id, quantity=1, price_at_purchase=random_prod.price, status=models.OrderStatus.DELIVERED)
                    session.add(order)

        session.commit()
        print(f"Success! Created {user_index} Customers with 100 Products and Smart Patterns.")

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()