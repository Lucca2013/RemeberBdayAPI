from src.repositories.birthday_repository import BirthdayRepository
from src.models.dtos import BirthdayDTO
from typing import List
from datetime import datetime

class BirthdayService:
    @staticmethod
    def create_birthday(user_id: str, name: str, date: str) -> dict:
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return {'success': False, 'message': 'Invalid date format. Use DD/MM/YYYY'}
        
        birthday = BirthdayDTO(user_id=user_id, name=name, date=date)
        success = BirthdayRepository.create(birthday)
        
        if success:
            return {'success': True, 'message': 'Birthday created successfully'}
        return {'success': False, 'message': 'Error creating birthday'}
    
    @staticmethod
    def get_user_birthdays(user_id: str) -> List[dict]:
        return BirthdayRepository.find_by_user_id(user_id)
    
    @staticmethod
    def delete_birthday(birthday_id: str, user_id: str) -> dict:
        success = BirthdayRepository.delete(birthday_id, user_id)
        
        if success:
            return {'success': True, 'message': 'Birthday deleted successfully'}
        return {'success': False, 'message': 'Birthday not found or unauthorized'}
    
    @staticmethod
    def update_birthday(birthday_id: str, user_id: str, name: str, date: str) -> dict:
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return {'success': False, 'message': 'Invalid date format. Use DD/MM/YYYY'}
        
        success = BirthdayRepository.update(birthday_id, user_id, name, date)
        
        if success:
            return {'success': True, 'message': 'Birthday updated successfully'}
        return {'success': False, 'message': 'Birthday not found or unauthorized'}