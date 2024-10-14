from datetime import datetime, timedelta, date

from aiogram import Router
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


@router.message(Command('admin_main_menu'))
@router.message(StateAdminMenu.admin_main_menu)
async def admin_main_menu(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(StateAdminMenu.admin_main_menu)
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == "Резервы столов":
            answer = await db_funcs_admin_menu.load_table_reservations()
            for ans in answer:
                await msg.answer(text=ans)
            await msg.answer(text=text_admin_navigator.admin_table_reservations,
                             reply_markup=kb_admin_menu.admin_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_table_reservations)
        elif prompt == "Резервы корпоративов":
            answer = await db_funcs_admin_menu.load_party_reservations()
            for ans in answer:
                await msg.answer(text=ans)
            await msg.answer(text=text_admin_navigator.admin_party_reservations,
                             reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_party_reservations)
        elif prompt == "Мероприятия":
            answer = await db_funcs_admin_menu.load_events()
            for ans in answer:
                await msg.answer(text=ans)
            await msg.answer(text=text_admin_navigator.admin_events,
                             reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_events)
        elif prompt == "Администраторы":
            answer = await db_funcs_admin_menu.load_admin_list()
            for ans in answer:
                await msg.answer(text=ans)
            await msg.answer(text=text_admin_navigator.admin_admin_list,
                             reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_admin_list)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)
