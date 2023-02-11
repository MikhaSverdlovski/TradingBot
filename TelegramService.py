import requests
from aiogram import Bot, Dispatcher, types
from Config import bot_token, chat_id


bot = Bot(token=bot_token)
dp = Dispatcher(bot)


def telegram_bot_sendtext(message):
    apiURL = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message})
    except Exception as e:
        print(e)



