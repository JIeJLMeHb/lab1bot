import requests
import json


def get_curse(): # получение официального курса белорусского рубля по отношению к 1 Доллару США на сегодня
    url = f"https://api.nbrb.by/exrates/rates/431"
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        output = str(data["Cur_Scale"]) + ' ' + str(data["Cur_Name"]) + " равен " + str(data["Cur_OfficialRate"]) + " Бел. руб."
        return output        
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
