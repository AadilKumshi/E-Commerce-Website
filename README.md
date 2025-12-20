#  Smart E-Commerce Backend API

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Status](https://img.shields.io/badge/Status-Live-success)

A REST API for e-commerce platforms, featuring a custom **Machine Learning Recommendation Engine** (Market Basket Analysis) to suggest "Frequently Bought Together" products.

Built with **FastAPI**, containerized with **Docker**, and deployed on **Render**.


##  Live Demo & Documentation
The API is live! You can interact with all endpoints via the Swagger UI:

 **[View Live API Docs (Swagger UI)](https://smart-ecom-api.onrender.com)**

### Test Credentials
I have set up a demo admin account so you can test protected endpoints (like creating products or viewing admin stats) without registering.

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `aadil` | `aadil` |

*(Note: The database resets periodically. If it's empty, the system automatically reseeds itself.)*


## ⚡ Key Features

### A pinch of Machine Learning
* **Market Basket Analysis:** Custom implementation of a co-occurrence matrix algorithm.
* **Real-time Recommendations:** When a user views a product, the system analyzes thousands of past transaction patterns to suggest items frequently purchased together (e.g., *Laptop -> Suggests Mouse + Sleeve*).
* **Synthetic Data Pipeline:** Includes a `seed.py` script using `Faker` and `NumPy` to generate realistic user personas and weighted purchasing history for model training.

### Backend Architecture
* **FastAPI Framework:** Utilized for high-performance, asynchronous request handling.
* **PostgreSQL Database:** Relational data storage managed via **SQLAlchemy ORM**.
* **Secure Authentication:** Full JWT (JSON Web Token) implementation with password hashing (Bcrypt).
* **Role-Based Access Control (RBAC):** Distinction between standard Users (browse/buy) and Admins (inventory management).

### DevOps & Deployment
* **Dockerized:** Fully containerized application using `Docker` and `docker-compose` for consistent development and production environments.
* **Cloud Hosted:** Live deployment on Render with managed PostgreSQL.


## Tech Stack

* **Language:** Python 3.10
* **Web Framework:** FastAPI
* **Database:** PostgreSQL
* **ML Libraries:** Pandas, NumPy, Scikit-Learn
* **Containerization:** Docker, Docker Compose
* **Validation:** Pydantic


## How to Run Locally?

You can run the entire project on your local machine using Docker. No need to install Python or PostgreSQL manually.

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/aadil/ai-ecommerce-backend.git](https://github.com/aadil/ai-ecommerce-backend.git)
    cd ai-ecommerce-backend
    ```

2.  **Start the Application**
    This command builds the images and starts the Web App and Database containers.
    ```bash
    docker-compose up --build
    ```

3.  **Seed the Database**
    Populate the empty database with products, users, and synthetic transaction data.
    *(Open a new terminal window)*
    ```bash
    docker-compose exec web python seed.py
    ```

4.  **Access the API**
    Open your browser to: `http://localhost:8000/docs`


## 📂 Project Structure

```bash
├── app
│   ├── database.py      # DB Connection & Session handling
│   ├── models.py        # SQLAlchemy Database Tables
│   ├── schemas.py       # Pydantic Models for Data Validation
│   ├── utils.py         # Password Hashing & JWT logic
│   └── routers          # API Endpoints
│       ├── auth.py
│       ├── products.py
│       └── ml.py        # Recommendation Engine Logic
├── docker-compose.yml   # Multi-container orchestration
├── Dockerfile           # Image build instructions
├── seed.py              # Synthetic Data Generator
├── requirements.txt     # Python Dependencies
└── main.py              # App Entry Point
