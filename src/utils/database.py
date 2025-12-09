import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import Config

class Database:
    @staticmethod
    @contextmanager
    def get_connection():
        conn = None
        try:
            conn = psycopg2.connect(Config.DATABASE_URL)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    @contextmanager
    def get_cursor(commit=True):
        with Database.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                if commit:
                    conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()