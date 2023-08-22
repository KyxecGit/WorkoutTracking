import requests
from datetime import datetime
import os

# Твои данные. Используем Nutritionix чтобы посчитать калории.
GENDER = "male"
WEIGHT_KG = 85
HEIGHT_CM = 185
AGE = 23

# Nutritionix  ID и API Ключ.
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"


exercise_text = input("Какое упражнение ты делал: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

# Добавляем время и дату
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

GOOGLE_SHEET_NAME = "workout"
sheet_endpoint = os.environ[
    "ENV_SHEETY_ENDPOINT"]

# Подключаемся к таблице
for exercise in result["exercises"]:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(
            os.environ["ENV_SHEETY_USERNAME"],
            os.environ["ENV_SHEETY_PASSWORD"],
        )
    )

