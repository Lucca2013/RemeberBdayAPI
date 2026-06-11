from flask import Flask
from flask_cors import CORS
from config import Config
from src.controllers.auth_controller import auth_bp
from src.controllers.birthday_controller import birthday_bp
from src.controllers.birthday_verificator_controller import notifications_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(birthday_bp, url_prefix='/api/birthdays')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)