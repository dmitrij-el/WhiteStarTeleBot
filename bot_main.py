import asyncio
import locale
import logging
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram_sqlite_storage.sqlitestore import SQLStorage
from aiogram.utils.chat_action import ChatActionMiddleware

from data import models_peewee
from config.config import BOT_TOKEN

from handlers import (main_menu_handlers,
                      table_reservations_handlers,
                      party_reservations_handlers,
                      user_profile_handlers)

from handlers.admin_menu_handlers import (adm_main_menu_handlers,
                                          adm_events_handlers,
                                          adm_party_reservations_handlers,
                                          adm_table_reservations_handlers,
                                          adm_admin_list_handlers,
                                          sending_messages)
from handlers.admin_menu_handlers.sending_messages import scheduler_args


async def main():

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=SQLStorage('./data/fsm.db'))
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp.message.middleware(ChatActionMiddleware())

    dp.include_router(main_menu_handlers.router)
    dp.include_router(user_profile_handlers.router)
    dp.include_router(party_reservations_handlers.router)
    dp.include_router(table_reservations_handlers.router)

    dp.include_router(adm_admin_list_handlers.router)
    dp.include_router(adm_events_handlers.router)
    dp.include_router(adm_main_menu_handlers.router)
    dp.include_router(adm_table_reservations_handlers.router)
    dp.include_router(adm_party_reservations_handlers.router)

    dp.message.register(main_menu_handlers.info_events,
                        F.text.lower().in_({"расписание мероприятий", "календарь", "расписание"}))
    dp.message.register(main_menu_handlers.info_events,
                        Command('info_events'))

    dp.message.register(main_menu_handlers.table_reservations,
                        F.text.lower().in_({"забронировать стол", "стол"}))
    dp.message.register(main_menu_handlers.table_reservations,
                        Command('table_reservations'))

    dp.message.register(main_menu_handlers.party_reservations,
                        F.text.lower().in_({"забронировать корпоратив", "корпоратив", "party", "вечеринка"}))
    dp.message.register(main_menu_handlers.party_reservations,
                        Command('party_reservations'))

    dp.message.register(main_menu_handlers.info_rest,
                        F.text.lower().in_({"об whitestar", "whitestar"}))
    dp.message.register(main_menu_handlers.info_rest,
                        Command('info_rest'))

    dp.message.register(main_menu_handlers.menu_rest,
                        F.text.lower().in_({"меню", "еда", "ресторанное меню"}))
    dp.message.register(main_menu_handlers.menu_rest,
                        Command('menu_rest'))

    dp.message.register(main_menu_handlers.user_profile,
                        F.text.lower().in_({"профиль"}))
    dp.message.register(main_menu_handlers.user_profile,
                        Command('profile'))

    dp.message.register(main_menu_handlers.send_help,
                        F.text.lower().in_({"помощь", "help"}))
    dp.message.register(main_menu_handlers.send_help,
                        Command('help'))

    scheduler_args(bot, scheduler)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    locale.setlocale(category=locale.LC_ALL, locale="ru-RU.UTF-8")
    models_peewee.create_models()
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    asyncio.run(main())
