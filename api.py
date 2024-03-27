# Import necessary libraries
from flask import Flask, request, jsonify
from enum import Enum
import psycopg2
import redis
import json

# Create Flask app
app = Flask(__name__)

# Enum for Order Type
class OrderType(Enum):
    INT = 'INT'
    DEL = 'DEL'

# Enum for Option Type
class OptionType(Enum):
    CE = 'CE'
    PE = 'PE'

# Database Connection
conn = psycopg2.connect(
    database="your_database",
    user="your_user",
    password="your_password",
    host="your_host",
    port="your_port"
)
cur = conn.cursor()

# Redis Connection
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# API Endpoint for POST Request
@app.route('/price-watch', methods=['POST'])
def price_watch():
    # Get data from the request
    data = request.json

    # Validate JWT Token (You may use a library like PyJWT for this)
    jwt_token = data.get('jwtToken')
    # Add your JWT validation logic here

    # Insert data into PostgreSQL
    cur.execute("""
        INSERT INTO price_watch (instrument_symbol, order_type, expiry, option_type, 
                                duration, trigger_price, quantity_in_lots, stop_loss_needed, 
                                strike_price, jwt_token)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['instrumentSymbol'], data['orderType'].value, data['expiry'], data['optionType'].value,
        data['duration'], data['triggerPrice'], data['quantityInLots'], data['stopLossNeeded'],
        data['strikePrice'], jwt_token
    ))
    conn.commit()

    # Store data in Redis (if needed)
    # You can customize this based on your requirements
    redis_key = f"price_watch:{data['instrumentSymbol']}"
    redis_client.hmset(redis_key, data)

    return jsonify({"message": "Data stored successfully"}), 201

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
