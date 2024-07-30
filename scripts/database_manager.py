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
                for post in data:
                    cur.execute("""
                        INSERT INTO reddit_posts 
                        (id, title, body, sentiment, confidence, score, num_comments, created_utc) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                        title = EXCLUDED.title,
                        body = EXCLUDED.body,
                        sentiment = EXCLUDED.sentiment,
                        confidence = EXCLUDED.confidence,
                        score = EXCLUDED.score,
                        num_comments = EXCLUDED.num_comments
                    """, (
                        post['id'], post['title'], post['body'], 
                        post['sentiment'], post['confidence'], 
                        post['score'], post['num_comments'], post['created_utc']
                    ))
                conn.commit()
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
                SELECT body FROM reddit_comments
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
            
    
    def fetch_stock_data(self, symbol):
        """
        Get processed data for a specific stock symbol from the database.
        
        Args:
        symbol (str): The stock symbol to fetch data for (e.g., 'AAPL', 'MSFT').

        Returns:
        pandas.DataFrame: A DataFrame containing the stock data.
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                # Read data for the specified stock symbol
                cur.execute("""
                SELECT created_utc, body, sentiment, sentiment_score
                FROM reddit_comments
                """)
                result = cur.fetchall()
                
                # Convert the result to a pandas DataFrame
                df = pd.DataFrame(result, columns=['created_utc', 'text', 'sentiment', 'sentiment_score'])
                
                # Filter for the stock symbol in Python
                #symbol_pattern = r'\b' + re.escape(symbol) + r'\b'
                #df = df[df['text'].str.contains(symbol_pattern, case=False, regex=True)]
                
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
                cur.execute("DELETE FROM reddit_posts")
                conn.commit()
        finally:
            self.connection_pool.putconn(conn)
            
            
    # You might add other database-related methods here, such as:
    # - update_data
    # - delete_data    