# scripts/database_manager.py
import pandas as pd
import psycopg2
from psycopg2 import pool, sql
from .config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class DatabaseManager:
    def __init__(self):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    def save_data(self, data):
        """
        Saves processed data to the PostgreSQL database.
        
        Args:
        data (list): List of dictionaries containing processed Reddit post data.
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                # Create a list of tuples from the data
                values = [(d['body']) for d in data]
                
                # Generate the SQL query
                insert_query = sql.SQL("""
                INSERT INTO reddit_comments (body)
                VALUES %s
                """)
                
                # Execute the query with the list of tuples as the parameter
                cur.execute(insert_query, (values,))
                
                # Commit the changes to the database
                conn.commit()
                
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            
        finally:
            self.connection_pool.putconn(conn)
            
    def fetch_data(self):
        """
        Get processed Data from the database.
        
        Args:
        data (list): List of dictionaries containing processed Reddit post data.
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                 # Read df from the existing table in the database
                read_query = sql.SQL("""
                SELECT * FROM reddit_comments
                """)
                cur.execute(read_query)
                result = cur.fetchall()
                # Convert the result to a pandas DataFrame
                df = pd.DataFrame(result)
                
                return df
            
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error
        
        finally:
            self.connection_pool.putconn(conn)
            
    
    def delete_data(self):
        """
        Delete all data from the database.
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute("""DELETE FROM reddit_comments""")
                conn.commit()
        finally:
            self.connection_pool.putconn(conn)