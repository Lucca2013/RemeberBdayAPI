from flask import Blueprint, request, jsonify
from src.services.auth_service import AuthService
from src.services.birthday_service import BirthdayService
from functools import wraps

birthday_bp = Blueprint('birthday', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        result = AuthService.verify_token(token)
        
        if not result['success']:
            return jsonify(result), 401
        
        request.user_id = result['user_id']
        return f(*args, **kwargs)
    
    return decorated

@birthday_bp.route('/', methods=['GET'])
@token_required
def get_birthdays():
    birthdays = BirthdayService.get_user_birthdays(request.user_id)
    return jsonify({'success': True, 'birthdays': birthdays}), 200

@birthday_bp.route('/', methods=['POST'])
@token_required
def create_birthday():
    data = request.get_json()
    
    if not data or 'name' not in data or 'date' not in data:
        return jsonify({'success': False, 'message': 'Name and date required'}), 400
    
    result = BirthdayService.create_birthday(request.user_id, data['name'], data['date'])
    status_code = 201 if result['success'] else 400
    
    return jsonify(result), status_code

@birthday_bp.route('/<birthday_id>', methods=['DELETE'])
@token_required
def delete_birthday(birthday_id):
    result = BirthdayService.delete_birthday(birthday_id, request.user_id)
    status_code = 200 if result['success'] else 404
    
    return jsonify(result), status_code

@birthday_bp.route('/<birthday_id>', methods=['PUT'])
@token_required
def update_birthday(birthday_id):
    data = request.get_json()
    
    if not data or 'name' not in data or 'date' not in data:
        return jsonify({'success': False, 'message': 'Name and date required'}), 400
    
    result = BirthdayService.update_birthday(birthday_id, request.user_id, data['name'], data['date'])
    status_code = 200 if result['success'] else 404
    
    return jsonify(result), status_code