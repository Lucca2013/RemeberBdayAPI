import time
from datetime import date, datetime
import json

from src.repositories.user_repository import UserRepository

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
        birthdays: list = UserRepository.get_all_birthdays()

        if birthdays:
            today = date.today()

            for bday_data in birthdays:

                name = bday_data.get("name", "Unknown")
                date_str = bday_data.get("date", "")

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
                        firebase_id = UserRepository.get_firebaseid_by_id(bday_data["ID"])

                        print(f"Id: {bday_data['ID']}; firebase_id: {firebase_id}")
                        
                        if(firebase_id != None and bday_data["ID"] not in birthdays_already_notificated):
                            message = messaging.Message(
                                notification=messaging.Notification(
                                    title=f"{bday_data['name']}'s birthday is coming!",
                                    body=f"{bday_data['name']}'s birthday is {bday_data['date']}"                                
                                ),
                                token=firebase_id
                            )

                            response = messaging.send(message)

                            birthdays_already_notificated.append(bday_data["ID"])
                            
                            with open('local_storage.json', 'r', encoding='utf-8') as f:
                                local_storage = json.load(f)

                            local_storage["birthdays_already_notificated"].clear()
                            local_storage["birthdays_already_notificated"] = birthdays_already_notificated

                            with open('local_storage.json', 'w', encoding='utf-8') as f:
                                json.dump(local_storage, f, ensure_ascii=False, indent=4)

                            print(f"some notification was sended, response: {response}")
                except Exception:
                    continue

    except Exception:
        return False
        
    return True