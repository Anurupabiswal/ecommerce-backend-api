# E-Commerce Backend API

A RESTful E-Commerce Backend API built using Python, Flask, and SQLite.

## Features

- Product CRUD operations
- User registration
- Password hashing
- User login
- Order creation
- SQL JOIN operations
- Stock management
- Order total calculation
- Input validation
- Error handling

## Technologies Used

- Python
- Flask
- SQLite
- REST API
- SQL
- Git & GitHub
- Thunder Client

## API Endpoints

### Products

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | Get all products |
| POST | `/products` | Add a new product |
| PUT | `/products/<id>` | Update a product |
| DELETE | `/products/<id>` | Delete a product |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Login a user |

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders` | Place a new order |
| GET | `/orders` | Get all orders |

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Anurupabiswal/ecommerce-backend-api.git