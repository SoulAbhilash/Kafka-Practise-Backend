import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from os import getenv
from dotenv import load_dotenv
import select
import json

class Database:
    def __init__(self):
        load_dotenv()
        self.db_config = {
            'dbname': getenv('DB_NAME'),
            'user': getenv('DB_USER'),
            'password': getenv('DB_PASSWORD'),
            'host': getenv('DB_HOST'),
            'port': getenv('DB_PORT')
        }

    def _create_connection(self):
        return psycopg2.connect(**self.db_config)

    def insert_product_bet(self, user_name, bet_price, product_name):
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            
            # Check if a bet exists for the user on the specific product
            check_query = sql.SQL("""
                SELECT id FROM products
                WHERE name = %s AND product_name = %s;
            """)
            cursor.execute(check_query, (user_name, product_name))
            existing_record = cursor.fetchone()

            if existing_record:
                # Update the bet amount if the record exists
                update_query = sql.SQL("""
                    UPDATE products
                    SET price = %s, bet_timestamp = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, name, price, product_name, bet_timestamp;
                """)
                cursor.execute(update_query, (bet_price, existing_record[0]))
                saved_data = cursor.fetchone()
                message = "Bet updated successfully!"
            else:
                # Insert a new record if no existing bet for the product
                insert_query = sql.SQL("""
                    INSERT INTO products (name, price, product_name, bet_timestamp)
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                    RETURNING id, name, price, product_name, bet_timestamp;
                """)
                cursor.execute(insert_query, (user_name, bet_price, product_name))
                saved_data = cursor.fetchone()
                message = "Bet saved successfully!"

            conn.commit()  # Commit the transaction

            # Close connections
            cursor.close()
            conn.close()

            # Return the saved data as a dictionary
            return {
                "id": saved_data[0],
                "user_name": saved_data[1],
                "bet_price": saved_data[2],
                "product_name": saved_data[3],
                "bet_timestamp": saved_data[4],
                "message": message
            }
            
        except Exception as e:
            print(e)
            return {"error": str(e)}

    
    def insert_highest_bid(self, id, product_name, bet_price):
        
        try:
            conn = self._create_connection()
            cursor = conn.cursor()

            query = sql.SQL("""
                INSERT INTO highest_bid (product_name, bid_amount, user_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (product_name)
                DO UPDATE SET bid_amount = EXCLUDED.bid_amount, user_id = EXCLUDED.user_id
            """)

            cursor.execute(query, (product_name, bet_price, id))
            conn.commit()  # Commit the transaction
            cursor.close()
            conn.close()

            return {"message": "Bet updated successfully!"}

        except Exception as e:
            print(e)
            return {"error": str(e)}

    
    def get_all_highest_bids(self):

        """
        Fetches the highest bid for each product with user details.
        """
        try:
            # Connect to the PostgreSQL database
            conn = self._create_connection()
            cursor = conn.cursor()

            # Query to get the highest bids with user data
            query = """
            SELECT 
                hb.product_name, 
                hb.bid_amount, 
                p.id AS user_id, 
                p.name AS user_name
            FROM 
                public.highest_bid hb
            JOIN 
                public.products p ON hb.user_id = p.id
            WHERE 
                (hb.product_name, hb.bid_amount) IN (
                    SELECT product_name, MAX(bid_amount)
                    FROM public.highest_bid
                    GROUP BY product_name
                )
            ORDER BY hb.bid_amount DESC;
            """

            cursor.execute(query)
            highest_bids = cursor.fetchall()

            response = {}
            for product_name, bid_amount, user_id, user_name in highest_bids:
                response[product_name] = {
                    "user": user_name,
                    "amount": bid_amount
                }

            cursor.close()
            conn.close()

            # Return the response
            print("Log from DB - FETCHED:", response)
            # Example return: {"Smartphone": {"user": "Alice", "amount": 300}, ... }
            return response

        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_single_product_highest_bid(self, product_name):
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute(
             '''
            SELECT 
                hb.product_name, 
                hb.bid_amount, 
                p.id AS user_id, 
                p.name AS user_name
            FROM 
                public.highest_bid hb
            LEFT JOIN 
                public.products p ON hb.user_id = p.id
            WHERE 
                hb.product_name = %s
            ORDER BY 
                hb.bid_amount DESC
            LIMIT 1;

            ''',
            (product_name,)  # Pass the product_name as a parameter
        )
        result = cursor.fetchone()
        conn.close()
        product_name, bid_amount, user_id, user_name = result
        
        if result:
            return {
                "product_name": product_name,
                "user": user_name if user_name is not None else None,
                "amount": bid_amount if bid_amount is not None else None
            }
        else:
            return None

    def get_product_list(self):
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute(
                '''
            SELECT array_agg(hb.product_name)
            FROM public.highest_bid hb;


            ''', # Pass the product_name as a parameter
        )
        result = cursor.fetchall()
        print(f"Fetched From DB - {result[0][0]}")
        conn.close()
        return [] if result[0][0] is None else result[0][0]
    
    def highest_bid_trigger_listener(self):
        conn = self._create_connection()
        cursor = conn.cursor()
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("LISTEN table_update;")
        print("Listening to PostgreSQL notifications on 'table_update' channel...")

        while True:
            if select.select([conn], [], [], 5) == ([conn], [], []):
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    payload = json.loads(notify.payload)
                    print(type(payload), payload)
                    print(f"amount and user: {payload['amount']} and { payload['user']}")
                    if (payload['amount'] and payload['user']):
                        print(f"Notification received: {payload}")
                        return payload
