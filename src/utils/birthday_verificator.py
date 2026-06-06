import time
from datetime import date, datetime

from src.repositories.user_repository import UserRepository

import firebase_admin

from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate(
    "firebase_key.json"
)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

last_api_check = 0
birthdays_already_notificated: list = []

def check_api_and_send_notifications():
    print("check_api_and_send_notifications function started")
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

                            print(f"some notification was sended, response: {response}")

                except Exception as e:
                    print(f"Error at check_api_and_send_notifications: {e}")

    except Exception as e:
        print(f"Erro no serviço: {e}")


def start_birthday_verificator_loop():
    global last_api_check
    
    print("start_birthday_verificator_loop function started")
    while True:
        current_time = time.time()
        now = datetime.now()

        if now.hour == 6 and now.minute == 0:
            birthdays_already_notificated.clear()

        if current_time - last_api_check > 3600:
            check_api_and_send_notifications()
            last_api_check = current_time

        time.sleep(60)