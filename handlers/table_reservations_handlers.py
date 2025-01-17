from datetime import datetime, timedelta, date
import os

from aiogram import Router, flags
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter

from data import db_funcs_admin_menu
from states.states import StateTableReservations, StateMenu
from keyboards import kb_main_menu, kb_user_profile, kb_table_reservations
from data.texts import text_user_profile, text_reservation, text_navigator
from data.models_peewee import db_beahea, TableReservationHistory, Table, User, data_tables
from utils import easy_funcs
from utils.table_reservation import working_images_funcs

router = Router()

"""
Резервирование стола
"""


class ProfileStateFilter(Filter):
    async def __call__(self, msg: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        prompt = msg.text
        return current_state in [
            StateTableReservations.add_table_reservations_booking_start_time_time,
            StateTableReservations.add_table_reservations_table,
            StateTableReservations.add_table_reservations_number_of_guests,
            StateTableReservations.add_table_reservations_confirmation_enter_data
        ] and (prompt == "Назад" or prompt == "Выбрать другое время")


@router.message(ProfileStateFilter())
@flags.chat_action("typing")
async def back_table_reservations(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    now_state = await state.get_state()
    await state.set_state()
    datas: dict = await state.get_data()
    if now_state == StateTableReservations.add_table_reservations_booking_start_time_time:
        await msg.answer(text=text_reservation.add_table_reservations_booking_start_time_date,
                         reply_markup=kb_table_reservations.date_enter())
        await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_date)
    elif now_state == StateTableReservations.add_table_reservations_table:
        date_datas = datetime.strptime(datas['date'], '%Y-%m-%d')
        await msg.answer(text=text_reservation.add_table_reservations_booking_start_time_time,
                         reply_markup=kb_table_reservations.time_enter(day_date=date_datas))
        await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_time)
    elif now_state == StateTableReservations.add_table_reservations_number_of_guests:
        path_plan = await working_images_funcs.processing_images(datas['tables_close'])
        plan_img = FSInputFile(path=path_plan)
        await msg.answer_photo(photo=plan_img,
                               caption=text_reservation.add_table_reservations_table,
                               reply_markup=kb_table_reservations.choosing_a_free_table(datas['tables_open']))
        await state.set_state(StateTableReservations.add_table_reservations_table)
    elif now_state == StateTableReservations.add_table_reservations_confirmation_enter_data:
        await msg.answer(text=text_reservation.add_table_reservations_number_of_guests,
                         reply_markup=kb_table_reservations.number_of_seats(datas['table']))
        await state.set_state(StateTableReservations.add_table_reservations_number_of_guests)


@router.message(StateTableReservations.main_table_reservations)
@flags.chat_action("typing")
async def main_table_reservations(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    user = User.get(User.user_id == user_id)
    if user.phone is None:
        await msg.answer(
            text=text_reservation.add_table_reservations_phone + text_user_profile.basic_data_update['phone'],
            reply_markup=kb_user_profile.choose_phone())
        await state.set_state(StateTableReservations.add_table_reservations_phone)
    else:
        await msg.answer(text=text_reservation.add_party_reservations_booking_start_time_date,
                         reply_markup=kb_table_reservations.date_enter())
        await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_date)


@router.message(StateTableReservations.add_table_reservations_phone)
@flags.chat_action("typing")
async def add_table_reservations_phone(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text=text_navigator.main_menu,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)
    else:
        check_phone = easy_funcs.checking_data_expression(phone_number=prompt)
        if check_phone:
            datas = await state.get_data()
            phone_number = easy_funcs.correction_datas(phone_number=prompt)
            user = User.update(phone=phone_number).where(User.user_id == user_id)
            user.execute()
            datas['phone_number'] = phone_number
            await state.update_data(**datas)
            await msg.answer(text=text_reservation.add_table_reservations_booking_start_time_date,
                             reply_markup=kb_table_reservations.date_enter())
            await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_date)
        else:
            await msg.answer(text=text_user_profile.err_basic_data_update['phone'],
                             reply_markup=kb_main_menu.choose_phone())
            await state.set_state(StateTableReservations.add_table_reservations_phone)


@router.message(StateTableReservations.add_table_reservations_booking_start_time_date)
@flags.chat_action("typing")
async def add_table_reservations_booking_start_time_date(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text=text_navigator.main_menu,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.clear()
        await state.set_state(StateMenu.main_menu)
    else:
        cor_date = easy_funcs.correction_datas(date_day=prompt)
        check_date = easy_funcs.checking_data_expression(date_day=cor_date)
        if check_date:
            datas = await state.get_data()
            cor_date = easy_funcs.correction_datas(date_day=prompt)
            if date.today() <= datetime.strptime(cor_date, '%Y-%m-%d').date():
                datas['user_id'] = User.select().where(User.user_id == user_id).get().id
                datas['date'] = cor_date
                await state.update_data(**datas)
                date_datas = datetime.strptime(datas['date'], '%Y-%m-%d')
                await msg.answer(text=text_reservation.add_table_reservations_booking_start_time_time,
                                 reply_markup=kb_table_reservations.time_enter(day_date=date_datas))
                await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_time)
            else:
                await msg.answer(text=text_reservation.add_party_reservations_err_booking_start_time_date,
                                 reply_markup=kb_table_reservations.date_enter())
                await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_date)
        else:
            await msg.answer(text=text_reservation.err_error
                                  + text_reservation.add_table_reservations_booking_start_time_date,
                             reply_markup=kb_table_reservations.date_enter())
            await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_date)


@router.message(StateTableReservations.add_table_reservations_booking_start_time_time)
@flags.chat_action("typing")
async def add_table_reservations_booking_start_time_time(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text=text_navigator.main_menu,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.clear()
        await state.set_state(StateMenu.main_menu)
    else:
        datas = await state.get_data()
        date_datas = datetime.strptime(datas['date'], '%Y-%m-%d')
        check_date = easy_funcs.checking_data_expression(time=prompt)
        if check_date:
            prompt = easy_funcs.correction_datas(time=prompt)
            datas['booking_start_time'] = datetime.strptime(datas['date'] + ' ' + prompt, '%Y-%m-%d %H:%M')

            tables_close = []
            tables_all = []
            tables_reservations = (TableReservationHistory
                                   .select().where(TableReservationHistory.booking_start_time
                                                   .between(datas['booking_start_time'] - timedelta(hours=1,
                                                                                                    minutes=59),
                                                            datas['booking_start_time'] + timedelta(hours=1,
                                                                                                    minutes=59))
                                                   ).order_by(TableReservationHistory.booking_start_time))
            for tab in tables_reservations:
                tables_close.append(tab.table.number_table)
            for tab in Table.select():
                tables_all.append(tab.number_table)
            tables_open = list(set(tables_all) - set(tables_close))
            tables_open.sort()
            datas['tables_close'] = tables_close
            datas['tables_open'] = tables_open
            await state.update_data(**datas)
            path_plan = await working_images_funcs.processing_images(tables_close)
            plan_img = FSInputFile(path=path_plan)
            await msg.answer_photo(photo=plan_img,
                                   caption=text_reservation.add_table_reservations_table,
                                   reply_markup=kb_table_reservations.choosing_a_free_table(tables_open))
            await state.set_state(StateTableReservations.add_table_reservations_table)
            if tables_close:
                os.remove(path=path_plan)
        else:
            await msg.answer(text=text_reservation.err_error
                                  + text_reservation.add_table_reservations_booking_start_time_time,
                             reply_markup=kb_table_reservations.time_enter(day_date=date_datas))
            await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_time)


@router.message(StateTableReservations.add_table_reservations_table)
@flags.chat_action("typing")
async def add_table_reservations_table(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text=text_navigator.main_menu,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.clear()
        await state.set_state(StateMenu.main_menu)
    else:
        def prompt_int(x):
            try:
                int(x)
                x = len(x) == 2
                return bool(x)
            except ValueError:
                return False

        datas = await state.get_data()
        check_prompt_list = [(value['symbol'], value['name_table']) for value in data_tables.values()]
        check_prompt_list = [val for values in check_prompt_list for val in values]
        if prompt in check_prompt_list:
            for key, value in data_tables.items():
                if value['symbol'] == prompt or value['name_table'] == prompt:
                    datas['table'] = int(key)
            await state.update_data(**datas)
            await msg.answer(text=text_reservation.add_table_reservations_number_of_guests,
                             reply_markup=kb_table_reservations.number_of_seats(datas['table']))
            await state.set_state(StateTableReservations.add_table_reservations_number_of_guests)
        elif prompt_int(prompt):
            datas['table'] = int(prompt)
            await state.update_data(**datas)
            await msg.answer(text=text_reservation.add_table_reservations_number_of_guests,
                             reply_markup=kb_table_reservations.number_of_seats(datas['table']))
            await state.set_state(StateTableReservations.add_table_reservations_number_of_guests)
        else:

            await msg.answer(text=text_reservation.add_table_reservations_err_table,
                             reply_markup=kb_table_reservations.choosing_a_free_table(datas['tables_open']))
            await state.set_state(StateTableReservations.add_table_reservations_table)


@router.message(StateTableReservations.add_table_reservations_number_of_guests)
@flags.chat_action("typing")
async def add_table_reservations_number_of_guests(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text=text_navigator.main_menu,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.clear()
        await state.set_state(StateMenu.main_menu)
    else:
        def prompt_check(x, max_quests):
            try:
                int(x)
                x = 1 <= x <= max_quests
                return bool(x)
            except ValueError:
                return False

        datas = await state.get_data()
        table = datas['table']
        max_quests = data_tables[str(table)]['number_of_seats']
        if prompt_check(int(prompt), max_quests):
            datas['number_of_guests'] = prompt
            table = Table.select().where(Table.number_table == datas["table"]).get()
            table = table.name_table
            await state.update_data(**datas)
            await msg.answer(text=text_reservation.table_reservation.format(
                table=table,
                booking_start_time=datas['booking_start_time'].strftime('%d-%m-%Y %H:%M'),
                number_of_guests=datas['number_of_guests']),
                reply_markup=kb_table_reservations.yes_no())
            await state.set_state(StateTableReservations.add_table_reservations_confirmation_enter_data)
        else:
            await msg.answer(text=text_reservation.err_error
                                  + text_reservation.add_table_reservations_number_of_guests,
                             reply_markup=kb_table_reservations.choosing_a_free_table(datas['tables_open']))
            await state.set_state(StateTableReservations.add_table_reservations_number_of_guests)


@router.message(StateTableReservations.add_table_reservations_confirmation_enter_data)
@flags.chat_action("typing")
async def add_table_reservations_confirmation_enter_data(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Да':
        datas = await state.get_data()
        try:
            table_id = Table.get(Table.number_table == datas['table'])
            datas['table'] = table_id.id
            with db_beahea.atomic():
                TableReservationHistory.create(**datas)
            from handlers.admin_menu_handlers import sending_messages
            notification = await db_funcs_admin_menu.l_table_reservation(user_id=user_id,
                                                                         date_reserve=datas['booking_start_time'],
                                                                         table_id=datas['table'])
            await sending_messages.notification_reservations_today(msg=msg, notification=notification)
            await msg.answer(text=text_reservation.table_successful_data_rec,
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateMenu.main_menu)
        except Exception as exp:
            await msg.answer(text=text_reservation.error_data_rec + '\n' + str(exp),
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateMenu.main_menu)
    elif prompt == 'Нет':
        await msg.answer(text=text_reservation.table_cancel_data_rec,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.clear()
        await state.set_state(StateMenu.main_menu)
