from flask import Blueprint, request, jsonify
from src.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    result = AuthService.register(data['username'], data['password'])
    status_code = 201 if result['success'] else 400
    
    return jsonify(result), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    result = AuthService.login(data['username'], data['password'], data['firebase_id'])
    status_code = 200 if result['success'] else 401
    
    return jsonify(result), status_code

@auth_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    
    if not data or 'token' not in data:
        return jsonify({'success': False, 'message': 'Token required'}), 400
    
    result = AuthService.verify_token(data['token'])
    status_code = 200 if result['success'] else 401
    
    return jsonify(result), status_code

@auth_bp.route('/health', methods=['GET'])
def healthz():
    return jsonify(status="healthy"), 200