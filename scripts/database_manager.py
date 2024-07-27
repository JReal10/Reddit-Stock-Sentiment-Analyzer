# scripts/database_manager.py

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
                        ON CONFLICT (id) DO UPDATE SET
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
        df = []
        try:
            with conn.cursor() as cur:
                 # Read df from the existing table in the database
                read_query = sql.SQL("""
                SELECT body FROM reddit_comments
                """)
                cur.execute(read_query)
                result = cur.fetchall()
                for row in result:
                    df.append(row[0])
                conn.commit()
        finally:
            self.connection_pool.putconn(conn)
            
        return df

    # You might add other database-related methods here, such as:
    # - update_data
    # - delete_data    