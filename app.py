from flask import Flask
from flask_cors import CORS
from config import Config
from src.controllers.auth_controller import auth_bp
from src.controllers.birthday_controller import birthday_bp
from src.utils.birthday_verificator import start_birthday_verificator_loop
import threading
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(birthday_bp, url_prefix='/api/birthdays')
    
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
        
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
        birthday_verificator = threading.Thread(target=start_birthday_verificator_loop, daemon=True)
        birthday_verificator.start()

    app.run(debug=True, host='0.0.0.0', port=5000)