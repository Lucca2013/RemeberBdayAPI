from src.utils.database import Database
from src.models.dtos import BirthdayDTO
from typing import List, Optional

class BirthdayRepository:
    @staticmethod
    def create(birthday: BirthdayDTO) -> bool:
        try:
            with Database.get_cursor() as cursor:
                sql = """INSERT INTO birthdays (user_id, name, date) VALUES (%s, %s, %s)"""
                cursor.execute(sql, (birthday.user_id, birthday.name, birthday.date))
                return True
        except Exception as e:
            print(f"Error creating birthday: {e}")
            return False
    
    @staticmethod
    def find_by_user_id(user_id: str) -> List[dict]:
        try:
            with Database.get_cursor(commit=False) as cursor:
                sql = """SELECT id, name, date, user_id FROM birthdays WHERE user_id = %s ORDER BY date"""
                cursor.execute(sql, (user_id,))
                results = cursor.fetchall()
                return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"Error fetching birthdays: {e}")
            return []
    
    @staticmethod
    def delete(birthday_id: str, user_id: str) -> bool:
        try:
            with Database.get_cursor() as cursor:
                sql = """DELETE FROM birthdays WHERE id = %s AND user_id = %s"""
                cursor.execute(sql, (birthday_id, user_id))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting birthday: {e}")
            return False
    
    @staticmethod
    def update(birthday_id: str, user_id: str, name: str, date: str) -> bool:
        try:
            with Database.get_cursor() as cursor:
                sql = """UPDATE birthdays SET name = %s, date = %s WHERE id = %s AND user_id = %s"""
                cursor.execute(sql, (name, date, birthday_id, user_id))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating birthday: {e}")
            return False
