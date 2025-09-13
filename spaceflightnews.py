import requests
import json


def get_spaceflight_summary():
    url = "https://api.spaceflightnewsapi.net/v4/reports/?limit=1&ordering=-published_at"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("results"):
            return data["results"][0]["summary"]
        else:
            return "Нет информации для получения"
    except requests.exceptions.RequestException as e:
        return f"Ошибка получения данных: {e}"
