
import pandas as pd
import random
from faker import Faker
from datetime import datetime
import os

fake = Faker()
random.seed(42)

os.makedirs("data", exist_ok=True)

today = datetime.today().strftime("%Y-%m-%d")

# Customers - always the same 100
def generate_customers(n=100):
    customers = []
    for i in range(1, n+1):
        customers.append({
            "customer_id": i,
            "name": fake.name(),
            "email": fake.email(),
            "city": fake.city(),
            "country": fake.country()
        })
    return pd.DataFrame(customers)

# Products - always the same 10
def generate_products():
    products = [
        {"product_id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99},
        {"product_id": 2, "name": "Phone", "category": "Electronics", "price": 699.99},
        {"product_id": 3, "name": "Desk Chair", "category": "Furniture", "price": 299.99},
        {"product_id": 4, "name": "Headphones", "category": "Electronics", "price": 149.99},
        {"product_id": 5, "name": "Monitor", "category": "Electronics", "price": 399.99},
        {"product_id": 6, "name": "Keyboard", "category": "Accessories", "price": 79.99},
        {"product_id": 7, "name": "Mouse", "category": "Accessories", "price": 49.99},
        {"product_id": 8, "name": "Desk", "category": "Furniture", "price": 499.99},
        {"product_id": 9, "name": "Webcam", "category": "Electronics", "price": 89.99},
        {"product_id": 10, "name": "Backpack", "category": "Accessories", "price": 59.99},
    ]
    return pd.DataFrame(products)

# Orders - TODAY only, append to existing
def generate_orders(n=50):
    orders = []
    for i in range(1, n+1):
        quantity = random.randint(1, 5)
        price = round(random.uniform(49.99, 999.99), 2)
        orders.append({
            "order_id": f"{today}-{i}",
            "customer_id": random.randint(1, 100),
            "product_id": random.randint(1, 10),
            "order_date": today,
            "quantity": quantity,
            "total_amount": round(price * quantity, 2)
        })
    return pd.DataFrame(orders)

if __name__ == "__main__":
    # Customers and products - overwrite
    generate_customers().to_csv("data/customers.csv", index=False)
    generate_products().to_csv("data/products.csv", index=False)

    # Orders - append today's orders
    orders = generate_orders()
    file_exists = os.path.exists("data/orders.csv")
    orders.to_csv("data/orders.csv", mode='a', header=not file_exists, index=False)

    print(f"✅ Done! Added 50 orders for {today}")
