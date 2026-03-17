from flask import Flask, request, jsonify
from database import Database
from two_phase_commit import TwoPhaseCommit
from saga_pattern import SagaPattern
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database on startup
with app.app_context():
    Database.init_db()

@app.route('/addToCart', methods=['POST'])
def add_to_cart():
    """Add items to cart"""
    data = request.get_json()
    
    # Debug logging
    print(f"Received data: {data}")
    print(f"Request content type: {request.content_type}")
    
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    print(f"Parsed - user_id: {user_id}, product_id: {product_id}, quantity: {quantity}")
    
    if not user_id or not product_id:
        return jsonify({
            'error': 'user_id and product_id are required',
            'received': data
        }), 400
    
    try:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check product availability
            cursor.execute(
                "SELECT product_name, stock, price FROM inventory WHERE product_id = %s",
                (product_id,)
            )
            product = cursor.fetchone()
            
            if not product:
                return jsonify({'error': 'Product not found'}), 404
            
            if product[1] < quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            
            # Add to cart
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity, price) VALUES (%s, %s, %s, %s) RETURNING id",
                (user_id, product_id, quantity, product[2])
            )
            cart_id = cursor.fetchone()[0]
            
            conn.commit()
            
            return jsonify({
                'message': 'Item added to cart',
                'cart_id': cart_id,
                'product_name': product[0],
                'quantity': quantity,
                'price': float(product[2])
            }), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/placeOrder', methods=['POST'])
def place_order():
    """Place order with Two-Phase Commit and SAGA pattern"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    use_saga = data.get('use_saga', False)  # Flag to choose between 2PC and SAGA
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get cart items
            cursor.execute(
                "SELECT product_id, quantity, price FROM cart WHERE user_id = %s",
                (user_id,)
            )
            cart_items = cursor.fetchall()
            
            if not cart_items:
                return jsonify({'error': 'Cart is empty'}), 400
            
            # Calculate total
            total_amount = sum(item[1] * item[2] for item in cart_items)
            
            # Create order
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s) RETURNING id",
                (user_id, total_amount, 'pending')
            )
            order_id = cursor.fetchone()[0]
            
            # Create payment transaction
            cursor.execute(
                "INSERT INTO payment_transactions (order_id, amount, status) VALUES (%s, %s, %s)",
                (order_id, total_amount, 'pending')
            )
            
            conn.commit()
            
            # Format cart items
            cart_items_list = [
                {
                    'user_id': user_id,
                    'product_id': item[0],
                    'quantity': item[1],
                    'price': float(item[2])
                }
                for item in cart_items
            ]
            
            if use_saga:
                # Use SAGA pattern
                success, message, steps = SagaPattern.execute_saga(order_id, cart_items_list)
                
                if success:
                    return jsonify({
                        'message': 'Order placed successfully using SAGA',
                        'order_id': order_id,
                        'total_amount': float(total_amount),
                        'pattern': 'SAGA',
                        'steps_completed': len(steps)
                    }), 201
                else:
                    return jsonify({
                        'error': message,
                        'order_id': order_id,
                        'pattern': 'SAGA',
                        'compensated': True
                    }), 400
            else:
                # Use Two-Phase Commit
                transaction_id = str(uuid.uuid4())
                
                # Phase 1: Prepare
                prepared, result = TwoPhaseCommit.prepare_phase(transaction_id, order_id, cart_items_list)
                
                if not prepared:
                    return jsonify({
                        'error': result,
                        'order_id': order_id,
                        'pattern': '2PC',
                        'phase': 'prepare'
                    }), 400
                
                # Phase 2: Commit
                committed, message = TwoPhaseCommit.commit_phase(transaction_id, order_id, cart_items_list)
                
                if committed:
                    return jsonify({
                        'message': 'Order placed successfully using 2PC',
                        'order_id': order_id,
                        'total_amount': float(total_amount),
                        'pattern': '2PC',
                        'transaction_id': transaction_id
                    }), 201
                else:
                    return jsonify({
                        'error': message,
                        'order_id': order_id,
                        'pattern': '2PC',
                        'phase': 'commit'
                    }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details"""
    try:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, user_id, total_amount, status, created_at FROM orders WHERE id = %s",
                (order_id,)
            )
            order = cursor.fetchone()
            
            if not order:
                return jsonify({'error': 'Order not found'}), 404
            
            return jsonify({
                'order_id': order[0],
                'user_id': order[1],
                'total_amount': float(order[2]),
                'status': order[3],
                'created_at': str(order[4])
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """Get cart items for user"""
    try:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.id, c.product_id, i.product_name, c.quantity, c.price, (c.quantity * c.price) as subtotal
                FROM cart c
                JOIN inventory i ON c.product_id = i.product_id
                WHERE c.user_id = %s
            """, (user_id,))
            
            items = cursor.fetchall()
            
            cart_items = [
                {
                    'cart_id': item[0],
                    'product_id': item[1],
                    'product_name': item[2],
                    'quantity': item[3],
                    'price': float(item[4]),
                    'subtotal': float(item[5])
                }
                for item in items
            ]
            
            total = sum(item['subtotal'] for item in cart_items)
            
            return jsonify({
                'user_id': user_id,
                'items': cart_items,
                'total': total
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=Config.FLASK_DEBUG, host='0.0.0.0', port=5001)
