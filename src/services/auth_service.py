from src.repositories.user_repository import UserRepository
from src.utils.jwt_handler import JWTHandler
from src.models.dtos import UserDTO
from typing import Optional

class AuthService:
    @staticmethod
    def register(username: str, password: str) -> dict:
        existing_user = UserRepository.find_by_username(username)
        if existing_user:
            return {'success': False, 'message': 'Username already exists'}
        
        user = UserDTO(username=username, password=password)
        success = UserRepository.create(user)
        
        if success:
            return {'success': True, 'message': 'User created successfully'}
        return {'success': False, 'message': 'Error creating user'}
    
    @staticmethod
    def login(username: str, password: str, firebase_id: str) -> dict:
        user = UserRepository.find_by_credentials(username, password)
        
        if not user:
            return {'success': False, 'message': 'Invalid credentials'}
        
        if(UserRepository.update_firebaseid(firebase_id, user['ID']) == False): 
            return {'success': False, 'message': 'Error setting firebase_id'}
        
        token = JWTHandler.encode_token(str(user['ID']))
        
        return {
            'success': True,
            'token': token,
            'user_id': str(user['ID']),
            'username': user['username']
        }
    
    @staticmethod
    def verify_token(token: str) -> dict:
        return JWTHandler.decode_token(token)