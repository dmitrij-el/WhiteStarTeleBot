"""
Конфигурационный файл для защиты ключей.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    exit('BOT_TOKEN отсутствует в переменных окружения')

TEST_PAYMENT_TOKEN_YOU_KASSA = os.getenv('TEST_PAYMENT_TOKEN_YOU_KASSA')
if TEST_PAYMENT_TOKEN_YOU_KASSA is None:
    exit('TEST_PAYMENT_TOKEN_YOU_KASSA отсутствует в переменных окружения')

TEST_PAYMENT_TOKEN_SBERBANK = os.getenv('TEST_PAYMENT_TOKEN_SBERBANK')
if TEST_PAYMENT_TOKEN_SBERBANK is None:
    exit('TEST_PAYMENT_TOKEN_SBERBANK отсутствует в переменных окружения')

API_HOST_RAPID_MICROSOFT_AZURE = "microsoft-translator-text.p.rapidapi.com"
API_URL_GIPHY = ''
API_URL_OPEN_WEATHER_DAY = 'https://api.openweathermap.org/data/2.5/weather'
API_URL_OPEN_WEATHER_PERIOD = 'https://api.openweathermap.org/data/2.5/forecast'

