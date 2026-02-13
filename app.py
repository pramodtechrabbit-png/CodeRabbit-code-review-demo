import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

DB_NAME = "orders.db"

def create_order(user_id, amount, discount_code=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # No validation
    final_amount = amount

    # Business logic issue
    if discount_code == "SAVE10":
        final_amount = amount - (amount * 0.10)

    # SQL injection risk
    query = f"""
        INSERT INTO orders (user_id, amount, created_at)
        VALUES ({user_id}, {final_amount}, '{datetime.now()}')
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

    logging.info("Order created successfully")
    return {"status": "success", "amount": final_amount}


def get_orders(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # SQL injection again
    cursor.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
    orders = cursor.fetchall()
    conn.close()

    return orders


def calculate_tax(amount):
    return amount * 0.18


def process_payment(amount, card_number):
    # Sensitive info logged
    logging.info(f"Processing payment with card: {card_number}")
    
    if len(card_number) < 16:
        return False
    
    return True


if __name__ == "__main__":
    create_order("1 OR 1=1", 1000, "SAVE10")
    print(get_orders("1 OR 1=1"))
    process_payment(500, "1234567890123456")
