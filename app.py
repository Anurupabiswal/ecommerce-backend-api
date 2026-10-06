
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)


def get_database_connection():
    connection = sqlite3.connect("ecommerce.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return "E-Commerce Backend API is running!"


# GET - Get all products
@app.route("/products", methods=["GET"])
def products():
    connection = get_database_connection()

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return jsonify([dict(product) for product in products])


# POST - Add a new product
# POST - Add a new product
# POST - Add a new product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name or price is None or stock is None:
        return jsonify({
            "message": "name, price and stock are required"
        }), 400

    if price < 0:
        return jsonify({
            "message": "Price cannot be negative"
        }), 400

    if stock < 0:
        return jsonify({
            "message": "Stock cannot be negative"
        }), 400

    connection = get_database_connection()

    connection.execute(
        """
        INSERT INTO products (name, price, stock)
        VALUES (?, ?, ?)
        """,
        (name, price, stock)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product added successfully"
    }), 201

# PUT - Update an existing product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()

    name = data["name"]
    price = data["price"]

    connection = get_database_connection()

    connection.execute(
        "UPDATE products SET name = ?, price = ? WHERE id = ?",
        (name, price, product_id)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product updated successfully"
    })
# DELETE - Delete a product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    connection = get_database_connection()

    connection.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product deleted successfully"
    })
# POST - Register a new user
# POST - Register a new user
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required"
        }), 400

    connection = get_database_connection()

    # Check if email already exists
    existing_user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user is not None:
        connection.close()
        return jsonify({
            "message": "Email already registered"
        }), 409

    # Hash password
    password_hash = generate_password_hash(password)

    connection.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """,
        (name, email, password_hash)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "User registered successfully"
    }), 201

# POST - Login user
# POST - Login user
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    connection = get_database_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    connection.close()

    if user is None:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    if check_password_hash(user["password"], password):
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    return jsonify({
        "message": "Invalid email or password"
    }), 401
# POST - Place a new order
# POST - Place a new order
# POST - Place a new order
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    # Check required fields
    if user_id is None or product_id is None or quantity is None:
        return jsonify({
            "message": "user_id, product_id and quantity are required"
        }), 400

    # Check quantity
    if quantity <= 0:
        return jsonify({
            "message": "Quantity must be greater than 0"
        }), 400

    connection = get_database_connection()

    # Check if user exists
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user is None:
        connection.close()
        return jsonify({
            "message": "User not found"
        }), 404

    # Check if product exists
    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if product is None:
        connection.close()
        return jsonify({
            "message": "Product not found"
        }), 404

    # Check stock
    if product["stock"] < quantity:
        connection.close()
        return jsonify({
            "message": "Not enough stock available",
            "available_stock": product["stock"]
        }), 400

    # Create order
    connection.execute(
        """
        INSERT INTO orders (user_id, product_id, quantity)
        VALUES (?, ?, ?)
        """,
        (user_id, product_id, quantity)
    )

    # Reduce stock
    connection.execute(
        """
        UPDATE products
        SET stock = stock - ?
        WHERE id = ?
        """,
        (quantity, product_id)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Order placed successfully"
    }), 201
    connection = get_database_connection()

    # Check if user exists
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user is None:
        connection.close()
        return jsonify({
            "message": "User not found"
        }), 404

    # Check if product exists
    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if product is None:
        connection.close()
        return jsonify({
            "message": "Product not found"
        }), 404

    # Create order
    connection.execute(
        """
        INSERT INTO orders (user_id, product_id, quantity)
        VALUES (?, ?, ?)
        """,
        (user_id, product_id, quantity)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Order placed successfully"
    }), 201
# GET - Get all orders
# GET - Get all orders
@app.route("/orders", methods=["GET"])
def get_orders():
    connection = get_database_connection()

    orders = connection.execute("""
        SELECT
            orders.id,
            users.name AS user_name,
            users.email,
            products.name AS product_name,
            products.price,
            orders.quantity,
            (products.price * orders.quantity) AS total
        FROM orders
        JOIN users ON orders.user_id = users.id
        JOIN products ON orders.product_id = products.id
    """).fetchall()

    connection.close()

    return jsonify([dict(order) for order in orders])

if __name__ == "__main__":
    app.run(debug=True)