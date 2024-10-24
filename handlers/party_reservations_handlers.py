from datetime import datetime, date

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.states import StateMenu, StatePartyReservations
from keyboards import kb_main_menu, kb_user_profile, kb_table_reservations
from data.texts import text_user_profile, text_reservation, text_navigator
from data.models_peewee import db_beahea, PartyReservationHistory, User
from data import db_funcs_admin_menu
from utils import easy_funcs

router = Router()

"""
Резервирование вечеринки
"""


@router.message(StatePartyReservations.main_party_reservations)
async def admin_table_reservations(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    user = User.get(User.user_id == user_id)
    if user.phone is None:
        await msg.answer(
            text=text_reservation.add_table_reservations_phone + text_user_profile.basic_data_update['phone'],
            reply_markup=kb_user_profile.choose_phone())
        await state.set_state(StatePartyReservations.add_party_reservations_phone)
    else:
        await msg.answer(text=text_reservation.add_party_reservations_booking_start_time_date,
                         reply_markup=kb_table_reservations.date_enter())
        await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_date)


@router.message(StatePartyReservations.add_party_reservations_phone)
async def add_table_reservations_phone(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await state.clear()
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
            await msg.answer(text=text_reservation.add_party_reservations_booking_start_time_date,
                             reply_markup=kb_table_reservations.date_enter())
            await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_date)
        else:
            await msg.answer(text=text_user_profile.err_basic_data_update['phone'],
                             reply_markup=kb_main_menu.choose_phone())
            await state.set_state(StatePartyReservations.add_party_reservations_phone)


@router.message(StatePartyReservations.add_party_reservations_booking_start_time_date)
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
                print(datas['user_id'])
                datas['date'] = cor_date
                await state.update_data(**datas)
                date_datas = datetime.strptime(datas['date'], '%Y-%m-%d')
                await msg.answer(text=text_reservation.add_table_reservations_booking_start_time_time,
                                 reply_markup=kb_table_reservations.time_enter(day_date=date_datas))
                await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_time)
            else:
                await msg.answer(text=text_reservation.add_party_reservations_err_booking_start_time_date,
                                 reply_markup=kb_table_reservations.date_enter())
                await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_date)
        else:
            await msg.answer(text=text_reservation.err_error
                                  + text_reservation.add_table_reservations_booking_start_time_date,
                             reply_markup=kb_table_reservations.date_enter())
            await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_date)


@router.message(StatePartyReservations.add_party_reservations_booking_start_time_time)
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
            del datas['date']
            await state.update_data(**datas)
            await msg.answer(text=text_reservation.add_party_reservations_number_of_guests,
                             reply_markup=kb_user_profile.back_button())
            await state.set_state(StatePartyReservations.add_party_reservations_number_of_guests)
        else:
            await msg.answer(text=text_reservation.err_error
                                  + text_reservation.add_table_reservations_booking_start_time_time,
                             reply_markup=kb_table_reservations.time_enter(day_date=date_datas))
            await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_time)


@router.message(StatePartyReservations.add_party_reservations_number_of_guests)
async def add_table_reservations_number_of_guests(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text=text_navigator.main_menu,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.clear()
        await state.set_state(StateMenu.main_menu)
    else:
        check_date = easy_funcs.checking_data_expression(number_of_guests=prompt)
        if check_date:
            datas = await state.get_data()
            datas['number_of_guests'] = prompt
            await state.update_data(**datas)
            await msg.answer(text=text_reservation.party_reservation.format(
                booking_start_time=datas['booking_start_time'].strftime('%d-%m-%Y %H:%M'),
                number_of_guests=datas['number_of_guests']),
                reply_markup=kb_table_reservations.yes_no())
            await state.set_state(StatePartyReservations.add_party_reservations_confirmation_enter_data)
        elif not check_date:
            await msg.answer(text=text_reservation.err_error
                                  + text_reservation.add_table_reservations_number_of_guests,
                             reply_markup=kb_user_profile.back_button())
            await state.set_state(StatePartyReservations.add_party_reservations_number_of_guests)


@router.message(StatePartyReservations.add_party_reservations_confirmation_enter_data)
async def admin_add_table_reservations_confirmation_enter_data(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Да':
        datas = await state.get_data()
        try:
            with db_beahea.atomic():
                PartyReservationHistory.create(**datas)
            from handlers.admin_menu_handlers import sending_messages
            notification = await db_funcs_admin_menu.l_party_reservation(user_id=user_id,
                                                                         date_reserve=datas['booking_start_time'])
            await sending_messages.notification_reservations_today(msg=msg, notification=notification)
            await msg.answer(text=text_reservation.party_successful_data_rec,
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateMenu.main_menu)
        except Exception as exp:
            await msg.answer(text=text_reservation.error_data_rec + '\n' + str(exp),
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateMenu.main_menu)
    elif prompt == 'Нет':
        await msg.answer(text=text_reservation.party_cancel_data_rec,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.clear()
        await state.set_state(StateMenu.main_menu)
