import time
from datetime import date, datetime

from src.repositories.user_repository import UserRepository

import firebase_admin

from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate(
    "firebase_key.json"
)

firebase_admin.initialize_app(cred)

last_api_check = 0

def check_api():
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
                        if(bday_data["firebase_id"] != None):
                            message = messaging.Message(
                                notification=messaging.Notification(
                                    title=f"{bday_data['name']}'s birthday is coming!",
                                    body=f"{bday_data['name']}'s birthday is {bday_data['date']}"                                
                                ),
                                token=bday_data["firebase_id"]
                            )

                            messaging.send(message)
                        else:
                            pass

                except:
                    pass

    except Exception as e:
        print(f"Erro no serviço: {e}")


while True:
    current_time = time.time()

    if current_time - last_api_check > 86400:
        check_api()
        last_api_check = current_time

    time.sleep(60)