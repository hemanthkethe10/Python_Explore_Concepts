import uuid
from database import Database

class TwoPhaseCommit:
    """Two-Phase Commit Protocol Implementation"""
    
    @staticmethod
    def prepare_phase(transaction_id, order_id, cart_items):
        """Phase 1: Prepare - Check if all participants can commit"""
        participants = []
        
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Participant 1: Inventory Service - Reserve stock
                for item in cart_items:
                    cursor.execute(
                        "SELECT stock FROM inventory WHERE product_id = %s FOR UPDATE",
                        (item['product_id'],)
                    )
                    result = cursor.fetchone()
                    
                    if not result or result[0] < item['quantity']:
                        cursor.execute(
                            "INSERT INTO tpc_participants (transaction_id, participant_name, status) VALUES (%s, %s, %s)",
                            (transaction_id, 'inventory', 'failed')
                        )
                        conn.commit()
                        return False, "Insufficient stock"
                
                cursor.execute(
                    "INSERT INTO tpc_participants (transaction_id, participant_name, status) VALUES (%s, %s, %s)",
                    (transaction_id, 'inventory', 'prepared')
                )
                participants.append('inventory')
                
                # Participant 2: Payment Service - Validate payment
                cursor.execute(
                    "SELECT total_amount FROM orders WHERE id = %s",
                    (order_id,)
                )
                order = cursor.fetchone()
                
                if not order:
                    cursor.execute(
                        "INSERT INTO tpc_participants (transaction_id, participant_name, status) VALUES (%s, %s, %s)",
                        (transaction_id, 'payment', 'failed')
                    )
                    conn.commit()
                    return False, "Order not found"
                
                cursor.execute(
                    "INSERT INTO tpc_participants (transaction_id, participant_name, status) VALUES (%s, %s, %s)",
                    (transaction_id, 'payment', 'prepared')
                )
                participants.append('payment')
                
                conn.commit()
                return True, participants
                
            except Exception as e:
                conn.rollback()
                return False, str(e)
    
    @staticmethod
    def commit_phase(transaction_id, order_id, cart_items):
        """Phase 2: Commit - Execute the transaction"""
        
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Check all participants are prepared
                cursor.execute(
                    "SELECT participant_name, status FROM tpc_participants WHERE transaction_id = %s",
                    (transaction_id,)
                )
                participants = cursor.fetchall()
                
                for participant in participants:
                    if participant[1] != 'prepared':
                        return False, f"Participant {participant[0]} not prepared"
                
                # Commit inventory changes
                for item in cart_items:
                    cursor.execute(
                        "UPDATE inventory SET stock = stock - %s WHERE product_id = %s",
                        (item['quantity'], item['product_id'])
                    )
                
                cursor.execute(
                    "UPDATE tpc_participants SET status = 'committed' WHERE transaction_id = %s AND participant_name = 'inventory'",
                    (transaction_id,)
                )
                
                # Commit payment
                cursor.execute(
                    "UPDATE payment_transactions SET status = 'completed' WHERE order_id = %s",
                    (order_id,)
                )
                
                cursor.execute(
                    "UPDATE tpc_participants SET status = 'committed' WHERE transaction_id = %s AND participant_name = 'payment'",
                    (transaction_id,)
                )
                
                # Update order status
                cursor.execute(
                    "UPDATE orders SET status = 'completed' WHERE id = %s",
                    (order_id,)
                )
                
                conn.commit()
                return True, "Transaction committed successfully"
                
            except Exception as e:
                conn.rollback()
                TwoPhaseCommit.abort_phase(transaction_id)
                return False, str(e)
    
    @staticmethod
    def abort_phase(transaction_id):
        """Abort transaction and rollback"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tpc_participants SET status = 'aborted' WHERE transaction_id = %s",
                (transaction_id,)
            )
            conn.commit()
