# E-Commerce Server with 2PC and SAGA Pattern

Flask server implementing Two-Phase Commit (2PC) and SAGA patterns for distributed transaction management.

## Features

- **Two-Phase Commit (2PC)**: Ensures atomicity across multiple services (inventory, payment)
- **SAGA Pattern**: Provides eventual consistency with compensation logic
- **PostgreSQL Database**: Persistent storage for orders, cart, inventory, and transaction logs

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure PostgreSQL:
```bash
# Create database
createdb ecommerce_db

# Copy and configure environment
cp .env.example .env
# Edit .env with your database credentials
```

3. Run the server:
```bash
python app.py
```

## API Endpoints

### 1. Add to Cart
```bash
POST /addToCart
Content-Type: application/json

{
  "user_id": 1,
  "product_id": 1,
  "quantity": 2
}
```

### 2. Place Order
```bash
POST /placeOrder
Content-Type: application/json

# Using Two-Phase Commit (default)
{
  "user_id": 1,
  "use_saga": false
}

# Using SAGA Pattern
{
  "user_id": 1,
  "use_saga": true
}
```

### 3. Get Order
```bash
GET /orders/<order_id>
```

### 4. Get Cart
```bash
GET /cart/<user_id>
```

## Pattern Comparison

### Two-Phase Commit (2PC)
- **Prepare Phase**: All participants vote to commit or abort
- **Commit Phase**: If all vote yes, commit; otherwise abort
- **Use Case**: Strong consistency required, short transactions
- **Pros**: ACID guarantees, strong consistency
- **Cons**: Blocking protocol, single point of failure

### SAGA Pattern
- **Forward Recovery**: Execute steps sequentially
- **Compensation**: Rollback completed steps on failure
- **Use Case**: Long-running transactions, microservices
- **Pros**: Non-blocking, better availability
- **Cons**: Eventual consistency, complex compensation logic

## Database Schema

- `orders`: Order records
- `cart`: Shopping cart items
- `inventory`: Product stock and pricing
- `payment_transactions`: Payment records
- `saga_log`: SAGA execution and compensation log
- `tpc_participants`: Two-phase commit participant status

## Example Usage

```bash
# Add items to cart
curl -X POST http://localhost:5000/addToCart \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_id": 1, "quantity": 2}'

# Place order with 2PC
curl -X POST http://localhost:5000/placeOrder \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "use_saga": false}'

# Place order with SAGA
curl -X POST http://localhost:5000/placeOrder \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "use_saga": true}'
```
