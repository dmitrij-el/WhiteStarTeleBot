"""
Конфигурационный файл для защиты ключей.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    exit('BOT_TOKEN отсутствует в переменных окружения')

ADMIN_DIMA = os.getenv('ADMIN_DIMA')
if ADMIN_DIMA is None:
    exit('ADMIN_DIMA отсутствует в переменных окружения')

DB_NAME = os.getenv('DB_NAME')
if DB_NAME is None:
    exit('DB_NAME отсутствует в переменных окружения')

DB_HOST = os.getenv('DB_HOST')
if DB_HOST is None:
    exit('DB_HOST отсутствует в переменных окружения')

DB_PORT = os.getenv('DB_PORT')
if DB_PORT is None:
    exit('DB_PORT отсутствует в переменных окружения')

DB_LOGIN = os.getenv('DB_LOGIN')
if DB_LOGIN is None:
    exit('DB_LOGIN отсутствует в переменных окружения')

DB_PASSWORD = os.getenv('DB_PASSWORD')
if DB_PASSWORD is None:
    exit('DB_PASSWORD отсутствует в переменных окружения')

API_HOST_RAPID_MICROSOFT_AZURE = "microsoft-translator-text.p.rapidapi.com"
API_URL_GIPHY = ''
API_URL_OPEN_WEATHER_DAY = 'https://api.openweathermap.org/data/2.5/weather'
API_URL_OPEN_WEATHER_PERIOD = 'https://api.openweathermap.org/data/2.5/forecast'

