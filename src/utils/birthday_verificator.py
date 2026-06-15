import time
from datetime import date, datetime
import json

from src.repositories.user_repository import UserRepository
from src.repositories.birthday_repository import BirthdayRepository

import firebase_admin

from firebase_admin import credentials
from firebase_admin import messaging

def check_api_and_send_notifications(birthdays_already_notificated):
    cred = credentials.Certificate(
        "firebase_key.json"
    )
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    try:
        users: list = UserRepository.get_all_users()
        
        if users:            
            for user in users:
                user_id = user.get("ID")
                firebase_id = UserRepository.get_firebaseid_by_id(str(user_id))

                
                if(firebase_id != None):
                    today = date.today()
                    birthdays = BirthdayRepository.find_by_user_id(user_id)
                    
                
                    for bday in birthdays:
                        name = bday.get("name", "Unknown")
                        date_str = bday.get("date", "")

                        try:
                            bday_obj = datetime.strptime(
                                date_str,
                                "%d/%m/%Y"
                            ).date()

                            bday_this_year = bday_obj.replace(
                                year=today.year
                            )

                            if bday_this_year < today:
                                bday_this_year = bday_this_year.replace(
                                    year=today.year + 1
                                )

                            diff = (bday_this_year - today).days

                            if 0 <= diff <= 3:
                                if(bday["id"] not in birthdays_already_notificated):
                                    message = messaging.Message(
                                        notification=messaging.Notification(
                                            title=f"{name}'s birthday is coming!",
                                            body=f"{name}'s birthday is {date_str}"                                
                                        ),
                                        token=firebase_id
                                    )

                                    messaging.send(message)

                                    birthdays_already_notificated.append(bday["id"])
                                    
                                    with open('local_storage.json', 'r', encoding='utf-8') as f:
                                        local_storage = json.load(f)

                                    local_storage["birthdays_already_notificated"].clear()
                                    local_storage["birthdays_already_notificated"] = birthdays_already_notificated

                                    with open('local_storage.json', 'w', encoding='utf-8') as f:
                                        json.dump(local_storage, f, ensure_ascii=False, indent=4)

                        except Exception as err:
                            print(err)
                            continue

    except Exception as err:
        print(err)
        return False
        
    return True