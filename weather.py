import requests
import asyncio
import json


def get_weather(location="Минск"):
    url = f"https://wttr.in/{location}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return f"В городе {location} на момент " + str(data["current_condition"][0]["observation_time"]) + " температура равна " + str(data["current_condition"][0]["temp_C"]) + " градус Цельсия, ощущается как " + str(data["current_condition"][0]["FeelsLikeC"]) + ". Влажность воздуха: " + str(data["current_condition"][0]["humidity"]) + "%, UV-индекс: " + str(data["current_condition"][0]["uvIndex"])

    except requests.exceptions.RequestException as e:
        return f"Ошибка получения данных о погоде: {e}"
