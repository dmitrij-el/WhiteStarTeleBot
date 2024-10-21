import asyncio
from datetime import datetime
from typing import Union, List

from aiogram import Router, BaseMiddleware, types
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from states.states import StateAdminMenu, StateMenu
from keyboards import kb_main_menu, kb_admin_menu
from data import db_funcs_admin_menu
from data.texts import text_admin_navigator
from data.db_funcs_user_account import check_admin
from data.models_peewee import db_beahea, PartyReservationHistory, Event
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
            datas['name_event'] = prompt
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
            if len(datas['weekday']) != 0:
                await state.update_data(**datas)
                await msg.answer(text=text_admin_navigator.admin_add_event_description,
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_event_description)
            else:
                await msg.answer(text=text_admin_navigator.admin_add_event_weekday,
                                 reply_markup=kb_admin_menu.admin_weekday_enter(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_event_weekday)
        elif prompt in ["Вся неделя", "Будни", *text_admin_navigator.weekday_dicts.keys()]:
            if prompt == "Вся неделя":
                datas['weekday'].extend([0, 1, 2, 3, 4, 5, 6])
            elif prompt == "Будни":
                datas['weekday'].extend([0, 1, 2, 3, 4])
            elif prompt in list(text_admin_navigator.weekday_dicts.keys()):
                datas['weekday'].append(text_admin_navigator.weekday_dicts[prompt])
            datas['weekday'] = [x for x in datas['weekday'] if datas['weekday'].count(x) == 1]
            await state.update_data(**datas)
            weekday = ', '.join([key for key, value
                                 in text_admin_navigator.weekday_dicts.items() for day
                                 in datas['weekday'] if value == int(day)])
            if weekday:
                await msg.answer(text="Выбранные дни недели: " + weekday,
                                 reply_markup=kb_admin_menu.admin_weekday_enter(user_id=user_id))
            else:
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
                             reply_markup=kb_admin_menu.admin_load_or_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_event_media)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_media)
async def name_event(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    if check_admin(user_id=user_id):
        prompt = msg.text
        if prompt == 'Отмена':
            await state.clear()
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        elif prompt == 'Загрузить':
            datas = await state.get_data()
            answer = easy_funcs.admin_checking_event(datas=datas)
            await msg.answer(text=text_admin_navigator.admin_add_event_confirmation_enter_data,
                             reply_markup=kb_admin_menu.admin_yes_no(user_id=user_id))
            await msg.answer_media_group(media=answer.build())
            await state.set_state(StateAdminMenu.admin_add_event_confirmation_enter_data)
        else:
            datas = await state.get_data()
            data = datas.setdefault('media_event')
            if data is None:
                datas['media_event'] = list()
            if msg.content_type == 'photo':
                datas['media_event'].append([msg.photo[-1].file_id, 'photo'])
            elif msg.content_type == 'video':
                datas['media_event'].append([msg.video.file_id, 'video'])
            elif msg.content_type == 'document':
                datas['media_event'].append([msg.document.file_id, 'document'])
            await state.update_data(**datas)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_event_confirmation_enter_data)
async def admin_add_table_reservations_confirmation_enter_data(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Да':
            datas = await state.get_data()
            check_datas = datas['media_event']
            for i in range(0, len(check_datas)):
                check_datas[i] = ' | '.join(check_datas[i])
            print(check_datas)
            datas['media_event'] = ' // '.join(check_datas)
            datas['weekday'] = ', '.join([str(i) for i in datas['weekday']])
            try:
                with db_beahea.atomic():
                    Event.create(**datas)
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
                check_event = Event.select().where(Event.id == int(prompt))
                if check_event:
                    check_event.get().delete_instance()
                    answer = await db_funcs_admin_menu.load_events()
                    if type(answer) is str:
                        await msg.answer(text=answer)
                        await msg.answer(text=text_admin_navigator.admin_events,
                                         reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
                        await state.set_state(StateAdminMenu.admin_events)
                    else:
                        for ans in answer:
                            await msg.answer_media_group(media=ans.build())
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
