import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import Config

class Database:
    @staticmethod
    @contextmanager
    def get_connection():
        conn = psycopg2.connect(Config.DATABASE_URL)
        try:
            yield conn
        finally:
            conn.close()
    
    @staticmethod
    def init_db():
        """Initialize database tables"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            
            # Orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    status VARCHAR(50) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Cart table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Inventory table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    product_id SERIAL PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL,
                    stock INTEGER NOT NULL,
                    price DECIMAL(10, 2) NOT NULL
                )
            """)
            
            # Payment transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payment_transactions (
                    id SERIAL PRIMARY KEY,
                    order_id INTEGER REFERENCES orders(id),
                    amount DECIMAL(10, 2) NOT NULL,
                    status VARCHAR(50) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # SAGA compensation log
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saga_log (
                    id SERIAL PRIMARY KEY,
                    order_id INTEGER,
                    step VARCHAR(100) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    compensation_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Two-phase commit participants
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tpc_participants (
                    id SERIAL PRIMARY KEY,
                    transaction_id VARCHAR(100) NOT NULL,
                    participant_name VARCHAR(100) NOT NULL,
                    status VARCHAR(50) DEFAULT 'prepared',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            cursor.close()
            
            # Insert sample inventory
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM inventory")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO inventory (product_name, stock, price) VALUES
                    ('Laptop', 10, 999.99),
                    ('Mouse', 50, 29.99),
                    ('Keyboard', 30, 79.99)
                """)
                conn.commit()
            cursor.close()
