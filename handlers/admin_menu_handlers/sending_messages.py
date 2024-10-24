import asyncio
import logging
from datetime import datetime, timedelta, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Router, BaseMiddleware, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.states import StateAdminMenu, StateMenu
from keyboards import kb_main_menu, kb_admin_menu
from data import db_funcs_admin_menu
from data.texts import text_admin_navigator
from data.db_funcs_user_account import check_admin
from data.models_peewee import db_beahea, TableReservationHistory, Table, PartyReservationHistory, Event, Admin, User
from utils import easy_funcs

router = Router()


async def notification_reservations(bot: Bot, admin_id: int):
    answer_table = await db_funcs_admin_menu.load_table_reservations(date=datetime.now())
    await bot.send_message(chat_id=admin_id, text='Резервы столов на сегодня')
    for ans in answer_table:
        await bot.send_message(chat_id=admin_id, text=ans)
    answer_party = await db_funcs_admin_menu.load_party_reservations(date=datetime.now())
    await bot.send_message(chat_id=admin_id, text='Резервы корпоративов на сегодня')
    for ans in answer_party:
        await bot.send_message(chat_id=admin_id, text=ans)



async def notification_reservations_today(msg: Message, notification: str):
    try:
        admin_list = list()
        with db_beahea:
            adm = Admin.select()
            for id_adm in adm:
                admin_list.append(int(id_adm.user_id))
        for admin_id in admin_list:
            print(admin_id, type(admin_id))
            await msg.bot.send_message(chat_id=admin_id, text=notification)
    except Exception as exp:
        logging.error(
            f'В процессе рассылки после заказа стола/корпоратива произошла ошибка\n'
            f'Ошибка: {exp}')


def scheduler_args(bot: Bot, scheduler: AsyncIOScheduler):
    admin_list = list()
    with db_beahea:
        adm = Admin.select()
        for id_adm in adm:
            admin_list.append(int(id_adm.user_id))

    for adm_id in admin_list:
        scheduler.add_job(notification_reservations, 'cron', hour=14, minute=00, args=(bot, adm_id))
