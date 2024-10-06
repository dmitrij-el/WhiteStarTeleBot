from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.states import StateAdminMenu, StateMenu
from keyboards import kb_main_menu, kb_admin_menu
from data import db_funcs_user_account, db_funcs_table_reservations
from data.texts import text_navigator, text_admin_navigator
from data.db_funcs_user_account import check_admin
from data.models_peewee import TableReservationHistory, Table, PartyReservationHistory, Event, Admin
from utils import easy_funcs

router = Router()


@router.message(Command('admin_main_menu'))
@router.message(StateAdminMenu.admin_main_menu)
async def main_menu(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == "Добавить/удалить забронированные столы":
            answer = db_funcs_table_reservations.load_table_reservations()
            await msg.answer(text=answer, reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_table_reservations)
        elif prompt == "Добавить/удалить корпоративы":
            answer = ''
            await msg.answer(text=answer, reply_markup=kb_admin_menu.adm_party_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_party_reservations)
        elif prompt == "Добавить/удалить мероприятие":
            answer = ''
            await msg.answer(text=answer, reply_markup=kb_admin_menu.adm_event_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_events)
        elif prompt == "Добавить/удалить администратора":
            answer = ''
            await msg.answer(text=answer, reply_markup=kb_admin_menu.adm_admin_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_admin_list)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_table_reservations)
async def main_menu(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == "Добавить бронь стола":
            await msg.answer(text=text_admin_navigator.admin_add_table_reservations_phone,
                             reply_markup=kb_admin_menu.adm_cancel(user_id=user_id))
        elif prompt == "Удалить бронь стола":
            await msg.answer(text=text_admin_navigator.admin_delete_table_reservations,
                             reply_markup=kb_admin_menu.adm_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_delete_table_reservations)
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_phone)
async def main_menu(msg: Message, state: FSMContext) -> None:
    datas_table_reservations = dict()
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        check_phone = easy_funcs.checking_data_expression(phone_number=prompt)
        if check_phone:
            datas_table_reservations['phone_number'] = easy_funcs.correction_phone_number(phone_number=prompt)

            await msg.answer(text=text_admin_navigator.admin_add_table_reservations_booking_start_time_date,
                             reply_markup=kb_admin_menu.adm_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
        elif not check_phone:
            await msg.answer(text=text_admin_navigator.admin_add_err_table_reservations_phone,
                             reply_markup=kb_admin_menu.adm_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_table_reservations_phone)
        elif prompt == 'Отменить':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
async def main_menu(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        check_date = easy_funcs.checking_data_expression(date=prompt)
        if check_date:
            datas_table_reservations['phone_number'] = easy_funcs.correction_phone_number(phone_number=prompt)

            await msg.answer(text=text_admin_navigator.admin_add_table_reservations_booking_start_time_date,
                             reply_markup=kb_admin_menu.adm_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
        elif not check_phone:
            await msg.answer(text=text_admin_navigator.admin_add_err_table_reservations_phone,
                             reply_markup=kb_admin_menu.adm_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_table_reservations_phone)
        elif prompt == 'Отменить':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_booking_start_time_time)
async def main_menu(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == '':
            pass
        elif prompt == '':
            pass
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_number_of_guests)
async def main_menu(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == '':
            pass
        elif prompt == '':
            pass
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_number_of_guests)
async def main_menu(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == '':
            pass
        elif prompt == '':
            pass
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_delete_table_reservations)
async def main_menu(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == '':
            pass
        elif prompt == '':
            pass
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.adm_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)
