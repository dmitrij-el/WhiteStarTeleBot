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
from data.models_peewee import db_beahea, TableReservationHistory, Table, User
from utils import easy_funcs

router = Router()

"""
Управление резервами столов 
"""


@router.message(StateAdminMenu.admin_table_reservations)
async def admin_table_reservations(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == "Добавить":
            await msg.answer(text=text_admin_navigator.admin_add_table_reservations_booking_start_time_date,
                             reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
        elif prompt == "Удалить":
            await msg.answer(text=text_admin_navigator.admin_delete_table_reservations,
                             reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_delete_table_reservations)
        elif prompt == "Список на день":
            await msg.answer(text=text_admin_navigator.admin_add_table_reservations_booking_start_time_date,
                             reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_view_table_reservations_in_date)
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.admin_table_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_table_reservations)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
async def admin_add_table_reservations_booking_start_time_date(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            cor_date = easy_funcs.correction_datas(date_day=prompt)
            check_date = easy_funcs.checking_data_expression(date_day=cor_date)
            if check_date:
                datas = await state.get_data()
                cor_date = easy_funcs.correction_datas(date_day=prompt)
                if date.today() <= datetime.strptime(cor_date, '%Y-%m-%d').date():
                    datas['date'] = cor_date
                    await state.update_data(**datas)
                    date_datas = datetime.strptime(datas['date'], '%Y-%m-%d')
                    await msg.answer(text=text_admin_navigator.admin_add_table_reservations_booking_start_time_time,
                                     reply_markup=kb_admin_menu.admin_time_enter(user_id=user_id, day_date=date_datas))
                    await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_time)
                else:
                    await msg.answer(text=text_admin_navigator.admin_add_table_reservations_err_booking_start_time_date,
                                     reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
            else:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_party_reservations_booking_start_time_date,
                                 reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_booking_start_time_time)
async def admin_add_table_reservations_booking_start_time_time(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            datas = await state.get_data()
            date_datas = datetime.strptime(datas['date'], '%Y-%m-%d')
            check_date = easy_funcs.checking_data_expression(time=prompt)
            if check_date:
                prompt = easy_funcs.correction_datas(time=prompt)
                datas['booking_start_time'] = datetime.strptime(datas['date'] + ' ' + prompt, '%Y-%m-%d %H:%M')
                del datas['date']
                tables_close = []
                tables_all = []
                tables_reservations = (TableReservationHistory
                                       .select().where(TableReservationHistory.booking_start_time
                                                       .between(datas['booking_start_time'] + timedelta(minutes=1),
                                                                datas['booking_start_time'] + timedelta(hours=2,
                                                                                                        minutes=59))
                                                       ).order_by(TableReservationHistory.booking_start_time))
                for tab in tables_reservations:
                    tables_close.append(tab.table.number_table)
                for tab in Table.select():
                    tables_all.append(tab.number_table)
                tables_open = list(set(tables_all) - set(tables_close))
                tables_open.sort()
                datas['tables_open'] = tables_open
                await state.update_data(**datas)
                await msg.answer(text=text_admin_navigator.admin_add_table_reservations_table + ':\n' + str(datas),
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_table)
            else:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_table_reservations_booking_start_time_time,
                                 reply_markup=kb_admin_menu.admin_time_enter(user_id=user_id, day_date=date_datas))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_time)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_table)
async def admin_add_table_reservations_table(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            datas = await state.get_data()
            if int(prompt) in datas['tables_open']:
                datas['table'] = int(prompt)
                del datas['tables_open']
                await state.update_data(**datas)
                await msg.answer(text=text_admin_navigator.admin_add_table_reservations_number_of_guests,
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_number_of_guests)
            else:
                await msg.answer(text=text_admin_navigator.admin_add_table_reservations_err_table,
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_table)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_number_of_guests)
async def admin_add_table_reservations_number_of_guests(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            check_date = easy_funcs.checking_data_expression(number_of_guests=prompt)
            if check_date:
                datas = await state.get_data()
                datas['number_of_guests'] = prompt
                await state.update_data(**datas)
                await msg.answer(text=text_admin_navigator.admin_add_table_reservations_phone,
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_phone)
            elif not check_date:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_table_reservations_number_of_guests,
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_number_of_guests)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_phone)
async def admin_add_table_reservations_phone(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            check_phone = easy_funcs.checking_data_expression(phone_number=prompt)
            if check_phone:
                datas = await state.get_data()
                phone_number = easy_funcs.correction_datas(phone_number=prompt)
                datas['phone_number'] = phone_number
                user = User.select(User.id).where(User.phone == phone_number)
                if user:
                    datas['user_id'] = user.get().id
                await state.update_data(**datas)
                answer = easy_funcs.admin_checking_table_reservations(datas=datas)
                if answer[0]:
                    await msg.answer(text=answer[1],
                                     reply_markup=kb_admin_menu.admin_yes_no(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_add_table_reservations_confirmation_enter_data)
                else:
                    await msg.answer(text=text_admin_navigator.admin_add_table_reservations_guest_name,
                                     reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_add_table_reservations_guest_name)
            else:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_table_reservations_phone,
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_phone)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_guest_name)
async def admin_add_table_reservations_number_of_guests(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            datas = await state.get_data()
            datas['name_user'] = prompt
            await state.update_data(**datas)
            answer = easy_funcs.admin_checking_table_reservations(datas=datas)
            await msg.answer(text=answer[1],
                             reply_markup=kb_admin_menu.admin_yes_no(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_table_reservations_confirmation_enter_data)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_table_reservations_confirmation_enter_data)
async def admin_add_table_reservations_confirmation_enter_data(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Да':
            datas = await state.get_data()
            try:
                with db_beahea.atomic():
                    TableReservationHistory.create(**datas)

                await msg.answer(text=text_admin_navigator.admin_successful_data_rec,
                                 reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
                await state.clear()
                await state.set_state(StateAdminMenu.admin_main_menu)
            except Exception as exp:
                await msg.answer(text=text_admin_navigator.admin_error_data_rec + '\n' + str(exp),
                                 reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
                await state.clear()
                await state.set_state(StateAdminMenu.admin_main_menu)
        elif prompt == 'Нет':
            await msg.answer(text=text_admin_navigator.admin_cancel_data_rec,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_delete_table_reservations)
async def admin_delete_table_reservations(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            with db_beahea:
                check_date = TableReservationHistory.select().where(TableReservationHistory.id == int(prompt))
                if check_date:
                    check_date.get().delete_instance()
                    answer = await db_funcs_admin_menu.load_table_reservations()
                    for ans in answer:
                        await msg.answer(text=ans,
                                         reply_markup=kb_admin_menu.admin_table_reservations_menu(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_table_reservations)
                else:
                    await msg.answer(text=text_admin_navigator.err_error
                                          + text_admin_navigator.admin_delete_table_reservations,
                                     reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_delete_table_reservations)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_view_table_reservations_in_date)
async def admin_view_table_reservations_in_date(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            cor_date = easy_funcs.correction_datas(date_day=prompt)
            check_date = easy_funcs.checking_data_expression(date_day=cor_date)
            if check_date:
                load_day = datetime.strptime(cor_date, '%Y-%m-%d')
                if date.today() <= load_day.date():
                    answer = await db_funcs_admin_menu.load_table_reservations(load_day)
                    for ans in answer:
                        await msg.answer(text=ans,
                                         reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_main_menu)
                else:
                    await msg.answer(text=text_admin_navigator.admin_add_table_reservations_booking_start_time_date,
                                     reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_view_table_reservations_in_date)
            else:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_party_reservations_booking_start_time_date,
                                 reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_table_reservations_booking_start_time_date)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)
