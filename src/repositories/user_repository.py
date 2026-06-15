from src.utils.database import Database
from src.models.dtos import UserDTO
from typing import Optional

class UserRepository:
    @staticmethod
    def create(user: UserDTO) -> bool:
        try:
            with Database.get_cursor() as cursor:
                sql = """INSERT INTO users (username, password) VALUES (%s, %s)"""
                cursor.execute(sql, (user.username, user.password))
                return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    @staticmethod
    def find_by_credentials(username: str, password: str) -> Optional[dict]:
        try:
            with Database.get_cursor(commit=False) as cursor:
                sql = """SELECT "ID", username FROM users WHERE username = %s AND password = %s"""
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Error finding user: {e}")
            return None
    

    @staticmethod
    def find_by_username(username: str) -> Optional[dict]:
        try:
            with Database.get_cursor(commit=False) as cursor:
                sql = """SELECT "ID", username FROM users WHERE username = %s"""
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            print(f"Error finding user by username: {e}")
            return None
        
    @staticmethod
    def update_firebaseid(firebase_id: str, id: str) -> bool:
        try:
            with Database.get_cursor() as cursor:
                sql = """UPDATE users
                        SET firebase_id = (%s)
                        WHERE "ID" = (%s);
                """
                cursor.execute(sql, (firebase_id, id))
                return True
        except:
            return False
        
    @staticmethod
    def get_firebaseid_by_id(id: str) -> Optional[str]:
        try:
            with Database.get_cursor(commit=False) as cursor:
                sql = """SELECT firebase_id FROM users WHERE "ID" = %s"""

                cursor.execute(sql, (id,)) 
                result = cursor.fetchone()
                
                if result and result.get("firebase_id"):
                    return str(result["firebase_id"])
                
                return None
        except Exception as e:
            print(f"Erro em get_firebaseid_by_id: {e}")
            return None
        
    @staticmethod
    def get_all_users() -> list[dict]:
        try:
            with Database.get_cursor(commit=False) as cursor:
                sql = """
                    SELECT *
                    FROM users
                """
                cursor.execute(sql)

                return cursor.fetchall() or []
        except Exception:
            return []

