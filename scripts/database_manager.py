# scripts/database_manager.py
from datetime import datetime, timedelta
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

    def insert_data(self, data):
        """
        Inserts raw data from the Reddit API into the PostgreSQL database,
        avoiding duplicates.
        
        Args:
        data (list): List of dictionaries containing raw Reddit post data.
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                # Assuming 'reddit_comments' table exists with appropriate columns
                insert_query = sql.SQL("""
                    INSERT INTO reddit_comments 
                    (id, body, created_utc, score, post_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """)
                
                # Prepare the values to be inserted
                values = [
                    (
                        item['id'],
                        item['body'],
                        item['created_utc'],
                        item['score'],
                        item['post_url'],
                    )
                    for item in data
                ]
                
                # Execute the query with the list of tuples as the parameter
                cur.executemany(insert_query, values)
                
                # Commit the changes to the database
                conn.commit()
                
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            
        finally:
            self.connection_pool.putconn(conn)
            
    def fetch_data(self):
        """
        Get processed Data from the database.
        
        Returns:
        pandas.DataFrame: DataFrame containing processed Reddit post data with original column names.
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                # Read data from the existing table in the database
                read_query = sql.SQL("""
                SELECT * FROM reddit_comments
                """)
                cur.execute(read_query)
                
                # Fetch the column names
                column_names = [desc[0] for desc in cur.description]
                
                # Fetch all rows
                result = cur.fetchall()
                
                # Convert the result to a pandas DataFrame with column names
                df = pd.DataFrame(result, columns=column_names)
                
                return df
            
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error
        
        finally:
            self.connection_pool.putconn(conn)

            
    
    def delete_data(self):
        """
        Delete data from the database that is older than 30 days.
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                thirty_days_ago = datetime.now() - timedelta(days=30)
                delete_query = sql.SQL("""
                    DELETE FROM reddit_comments
                    WHERE created_utc < %s
                """)
                cur.execute(delete_query, (thirty_days_ago,))
                conn.commit()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
        finally:
            self.connection_pool.putconn(conn)