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

""" 
Управление мероприятиями 
"""


@router.message(StateAdminMenu.admin_events)
async def admin_events(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == "Добавить":
            await msg.answer(text=text_admin_navigator.admin_add_event_name,
                             reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_event_name)
        elif prompt == "Удалить":
            await msg.answer(text=text_admin_navigator.admin_delete_events,
                             reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_delete_events)
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_events)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_name)
async def name_event(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            datas = await state.get_data()
            datas['name'] = prompt
            await state.update_data(**datas)
            await msg.answer(text=text_admin_navigator.admin_add_event_start_date,
                             reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_event_start_date)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_start_date)
async def admin_delete_events(msg: Message, state: FSMContext):
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
                datas['start_time_event'] = cor_date
                data_start_date = datetime.strptime(datas['start_time_event'], '%Y-%m-%d')
                await state.update_data(**datas)
                await msg.answer(text=text_admin_navigator.admin_add_event_end_date,
                                 reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id,
                                                                             day_date=data_start_date,
                                                                             weeks_fnc=True))
                await state.set_state(StateAdminMenu.admin_add_event_end_date)
            else:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_event_start_date,
                                 reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_event_start_date)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_end_date)
async def admin_delete_events(msg: Message, state: FSMContext):
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
                data_start_date = datetime.strptime(datas['start_time_event'], '%Y-%m-%d')
                data_end_date = datetime.strptime(cor_date, '%Y-%m-%d')
                if data_start_date.date() <= data_end_date.date():
                    datas['end_time_event'] = cor_date
                    await state.update_data(**datas)

                    await msg.answer(text=text_admin_navigator.admin_add_event_weekday,
                                     reply_markup=kb_admin_menu.admin_weekday_enter(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_add_event_weekday)
                else:
                    await msg.answer(text=text_admin_navigator.admin_add_event_err_end_date,
                                     reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id,
                                                                                 day_date=data_start_date,
                                                                                 weeks_fnc=True))
                    await state.set_state(StateAdminMenu.admin_add_event_end_date)
            else:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_event_end_date,
                                 reply_markup=kb_admin_menu.admin_date_enter(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_event_end_date)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_weekday)
async def admin_add_event_weekday(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        datas = await state.get_data()
        datas.setdefault('weekday')
        if datas['weekday'] is None:
            datas['weekday'] = list()
        datas['weekday'] = [x for x in datas['weekday'] if datas['weekday'].count(x) == 1]
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        elif prompt == "Подтвердить":
            await state.update_data(**datas)
            await msg.answer(text=text_admin_navigator.admin_add_event_description,
                             reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_event_description)
        elif prompt in ["Вся неделя", "Вся неделя", *text_admin_navigator.weekday_dicts.keys()]:
            if prompt == "Вся неделя":
                datas['weekday'].extend([0, 1, 2, 3, 4, 5, 6])
            elif prompt == "Будни":
                datas['weekday'].extend([0, 1, 2, 3, 4])
            elif prompt in list(text_admin_navigator.weekday_dicts.keys()):
                datas['weekday'].append(text_admin_navigator.weekday_dicts[prompt])
            await state.update_data(**datas)
            await msg.answer(text=text_admin_navigator.admin_add_event_weekday,
                             reply_markup=kb_admin_menu.admin_weekday_enter(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_event_weekday)
        else:
            await msg.answer(text=text_admin_navigator.err_error
                                  + text_admin_navigator.admin_add_event_weekday,
                             reply_markup=kb_admin_menu.admin_weekday_enter(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_event_weekday)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_description)
async def name_event(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await state.clear()
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            datas = await state.get_data()
            datas['description_event'] = prompt
            await state.update_data(**datas)
            await msg.answer(text=text_admin_navigator.admin_add_event_media,
                             reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_event_media)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_media)
async def name_event(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    content = msg.photo, msg.video
    datas = await state.get_data()
    datas.setdefault('media_event')
    if datas['media_event'] is None:
        datas['media_event'] = list()
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await state.clear()
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        elif content:
            corr_datas = list()
            for ph in content:
                corr_datas.append(ph.file_id)
            datas['media_event'].extend(corr_datas)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_delete_events)
async def admin_delete_events(msg: Message, state: FSMContext):
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
                check_date = Event.select().where(PartyReservationHistory.id == int(prompt))
                if check_date:
                    check_date.get().delete_instance()
                    answer = await db_funcs_admin_menu.load_events()
                    for ans in answer:
                        await msg.answer(text=ans)
                    await msg.answer(text=text_admin_navigator.admin_events,
                                     reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_events)
                else:
                    await msg.answer(text=text_admin_navigator.err_error
                                          + text_admin_navigator.admin_delete_events,
                                     reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_delete_events)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)
