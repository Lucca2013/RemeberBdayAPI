from flask import Blueprint, jsonify
from src.utils.birthday_verificator import check_api_and_send_notifications
import json

notifications_bp = Blueprint('notifications_bp', __name__)

@notifications_bp.route('/message_push_birthdays/', methods=['GET', 'POST'])
def message_push_birthdays():
    with open('local_storage.json', 'r', encoding='utf-8') as f:
        local_storage = json.load(f)
        
    birthdays_already_notificated = local_storage["birthdays_already_notificated"]
        
    response = check_api_and_send_notifications(birthdays_already_notificated)
    
    return jsonify({"status": "ok" if response else "not ok"}), 200 if response else 500

@notifications_bp.route('/clean_birthdays_already_notificated_at_localstorage/', methods=['GET', 'POST'])
def trigger_birthday_check():
    with open('local_storage.json', 'r', encoding='utf-8') as f:
        local_storage = json.load(f)

    local_storage["birthdays_already_notificated"].clear()

    with open('local_storage.json', 'w', encoding='utf-8') as f:
        json.dump(local_storage, f, ensure_ascii=False, indent=4)
