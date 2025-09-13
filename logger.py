from datetime import datetime
import pandas as pd
import functools
import asyncio
import os


LOG_FILE = "./logs/log.csv"
KEYBOARD_BUTTONS = [
"☁️Данные о погоде☀️",
"🚀Информация о событиях в сфере космических полётов",
"💲Курс доллара💵",
] #список кнопок для поиска(сделан для удобства)

def logging(func):
    if asyncio.iscoroutinefunction(func): #проверка функции на асинхроность
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            msg = extract_message(args)
            user_id, username, motion, api_text = extract_user_data(msg)
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H:%M:%S")

            result = await func(*args, **kwargs)

            if motion == "API":
                api_answer = result.text if result and hasattr(result, "text") else "No response"
            else:
                api_answer = "NONE"

            save_log(user_id, username, motion, api_text, date_str, time_str, api_answer)
            return result
        return async_wrapper

    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            msg = extract_message(args)
            user_id, username, motion, api_text = extract_user_data(msg)
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H:%M:%S")

            result = func(*args, **kwargs)

            if motion == "API":
                api_answer = result.text if result and hasattr(result, "text") else "No response"
            else:
                api_answer = "NONE"

            save_log(user_id, username, motion, api_text, date_str, time_str, api_answer)
            return result
        return sync_wrapper


def extract_message(args): #Для поиска сообщений (костыль)
    for arg in args:
        if hasattr(arg, "from_user") and hasattr(arg, "text"):
            return arg
    return None


def extract_user_data(msg): #Unic_ID, @TG_ncik, Motion, API
    if msg:
        user_id = msg.from_user.id
        username = f"@{msg.from_user.username}" if msg.from_user.username else "NoUsername"
        if msg.text and msg.text.strip() in KEYBOARD_BUTTONS:
            motion = "API"
            api_text = msg.text.strip()
        else:
            motion = "Keyboard typing"
            api_text = "NONE"
        return user_id, username, motion, api_text
    return "Unknown", "Unknown", "Keyboard typing", "NONE"


def save_log(user_id, username, motion, api_text, date_str, time_str, api_answer):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True) #лог в папке logs
    new_entry = pd.DataFrame([{
        "Unic_ID": user_id,
        "@TG_nick": username,
        "Motion": motion,
        "API": api_text,
        "Date": date_str,
        "Time": time_str,
        "API_answer": api_answer
    }])

    file_exists = os.path.exists(LOG_FILE)

    new_entry.to_csv(
        LOG_FILE,
        mode="a",
        index=False,
        encoding="utf-8-sig",
        header=not file_exists #Заголовки только при первом создании
    )
