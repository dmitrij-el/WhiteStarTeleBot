"""
Телеграм бот работает в асинхронном режиме.
Имя токена BOT_TOKEN
Токен должен лежать ---> ./config/.env
База данных -----> ./data/beahea_bot.db
Включена память состояний пользователя
Включена HTML разметка
Включено игнорирование обработки сообщений если бот был выключен
Включен Router

Dirs:
config - конфигурационные файлы
data - данные и методы работы с ними
handlers - обработчики действий
keyboards - клавиатуры и кнопки
states - состояния пользователя
utils - работа с API и другой функционал бота

"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram_sqlite_storage.sqlitestore import SQLStorage
from aiogram.utils.chat_action import ChatActionMiddleware

from data import models_peewee
from config.config import BOT_TOKEN

from handlers import main_menu_handlers, table_reservations_handlers


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=SQLStorage('./data/fsm.db'))

    dp.message.middleware(ChatActionMiddleware())

    dp.include_router(main_menu_handlers.router)
    dp.include_router(table_reservations_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    models_peewee.create_models()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
