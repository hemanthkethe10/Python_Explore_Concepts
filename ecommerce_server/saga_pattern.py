from database import Database
import json

class SagaPattern:
    """SAGA Pattern Implementation for distributed transactions"""
    
    @staticmethod
    def execute_saga(order_id, cart_items):
        """Execute SAGA transaction with compensation logic"""
        
        steps_completed = []
        
        try:
            # Step 1: Reserve Inventory
            success, data = SagaPattern._reserve_inventory(order_id, cart_items)
            if not success:
                return False, "Failed to reserve inventory", []
            steps_completed.append(('reserve_inventory', data))
            
            # Step 2: Process Payment
            success, data = SagaPattern._process_payment(order_id)
            if not success:
                SagaPattern._compensate(order_id, steps_completed)
                return False, "Payment failed", steps_completed
            steps_completed.append(('process_payment', data))
            
            # Step 3: Update Order Status
            success, data = SagaPattern._update_order(order_id, 'completed')
            if not success:
                SagaPattern._compensate(order_id, steps_completed)
                return False, "Failed to update order", steps_completed
            steps_completed.append(('update_order', data))
            
            # Step 4: Clear Cart
            success, data = SagaPattern._clear_cart(order_id, cart_items)
            if not success:
                SagaPattern._compensate(order_id, steps_completed)
                return False, "Failed to clear cart", steps_completed
            steps_completed.append(('clear_cart', data))
            
            return True, "SAGA completed successfully", steps_completed
            
        except Exception as e:
            SagaPattern._compensate(order_id, steps_completed)
            return False, str(e), steps_completed
    
    @staticmethod
    def _reserve_inventory(order_id, cart_items):
        """Reserve inventory for order"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                reserved_items = []
                for item in cart_items:
                    cursor.execute(
                        "SELECT stock FROM inventory WHERE product_id = %s FOR UPDATE",
                        (item['product_id'],)
                    )
                    result = cursor.fetchone()
                    
                    if not result or result[0] < item['quantity']:
                        conn.rollback()
                        return False, None
                    
                    cursor.execute(
                        "UPDATE inventory SET stock = stock - %s WHERE product_id = %s",
                        (item['quantity'], item['product_id'])
                    )
                    reserved_items.append(item)
                
                cursor.execute(
                    "INSERT INTO saga_log (order_id, step, status, compensation_data) VALUES (%s, %s, %s, %s)",
                    (order_id, 'reserve_inventory', 'completed', json.dumps(reserved_items))
                )
                
                conn.commit()
                return True, reserved_items
                
            except Exception as e:
                conn.rollback()
                return False, None
    
    @staticmethod
    def _process_payment(order_id):
        """Process payment for order"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute(
                    "SELECT id, amount FROM payment_transactions WHERE order_id = %s",
                    (order_id,)
                )
                payment = cursor.fetchone()
                
                if not payment:
                    return False, None
                
                # Simulate payment processing
                cursor.execute(
                    "UPDATE payment_transactions SET status = 'completed' WHERE id = %s",
                    (payment[0],)
                )
                
                cursor.execute(
                    "INSERT INTO saga_log (order_id, step, status, compensation_data) VALUES (%s, %s, %s, %s)",
                    (order_id, 'process_payment', 'completed', json.dumps({'payment_id': payment[0]}))
                )
                
                conn.commit()
                return True, {'payment_id': payment[0]}
                
            except Exception as e:
                conn.rollback()
                return False, None
    
    @staticmethod
    def _update_order(order_id, status):
        """Update order status"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute(
                    "UPDATE orders SET status = %s WHERE id = %s",
                    (status, order_id)
                )
                
                cursor.execute(
                    "INSERT INTO saga_log (order_id, step, status) VALUES (%s, %s, %s)",
                    (order_id, 'update_order', 'completed')
                )
                
                conn.commit()
                return True, {'order_id': order_id}
                
            except Exception as e:
                conn.rollback()
                return False, None
    
    @staticmethod
    def _clear_cart(order_id, cart_items):
        """Clear cart after successful order"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                user_id = cart_items[0]['user_id'] if cart_items else None
                if user_id:
                    cursor.execute(
                        "DELETE FROM cart WHERE user_id = %s",
                        (user_id,)
                    )
                
                cursor.execute(
                    "INSERT INTO saga_log (order_id, step, status) VALUES (%s, %s, %s)",
                    (order_id, 'clear_cart', 'completed')
                )
                
                conn.commit()
                return True, {'user_id': user_id}
                
            except Exception as e:
                conn.rollback()
                return False, None
    
    @staticmethod
    def _compensate(order_id, steps_completed):
        """Compensate completed steps in reverse order"""
        for step_name, step_data in reversed(steps_completed):
            if step_name == 'reserve_inventory':
                SagaPattern._compensate_inventory(order_id, step_data)
            elif step_name == 'process_payment':
                SagaPattern._compensate_payment(order_id, step_data)
            elif step_name == 'update_order':
                SagaPattern._compensate_order(order_id)
    
    @staticmethod
    def _compensate_inventory(order_id, reserved_items):
        """Restore inventory"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            for item in reserved_items:
                cursor.execute(
                    "UPDATE inventory SET stock = stock + %s WHERE product_id = %s",
                    (item['quantity'], item['product_id'])
                )
            
            cursor.execute(
                "INSERT INTO saga_log (order_id, step, status) VALUES (%s, %s, %s)",
                (order_id, 'compensate_inventory', 'completed')
            )
            
            conn.commit()
    
    @staticmethod
    def _compensate_payment(order_id, payment_data):
        """Refund payment"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE payment_transactions SET status = 'refunded' WHERE id = %s",
                (payment_data['payment_id'],)
            )
            
            cursor.execute(
                "INSERT INTO saga_log (order_id, step, status) VALUES (%s, %s, %s)",
                (order_id, 'compensate_payment', 'completed')
            )
            
            conn.commit()
    
    @staticmethod
    def _compensate_order(order_id):
        """Revert order status"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE orders SET status = 'failed' WHERE id = %s",
                (order_id,)
            )
            
            cursor.execute(
                "INSERT INTO saga_log (order_id, step, status) VALUES (%s, %s, %s)",
                (order_id, 'compensate_order', 'completed')
            )
            
            conn.commit()
