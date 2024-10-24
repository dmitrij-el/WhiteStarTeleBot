from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.states import StateMenu, StateUserProfile
from keyboards import kb_user_profile
from data import db_funcs_user_account
from data.texts import text_navigator, text_user_profile
from data.models_peewee import User, Gender
from utils import easy_funcs

router = Router()


@router.message(StateMenu.user_profile)
async def user_profile_main(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    user = User.get(User.user_id == user_id)
    from playhouse.shortcuts import model_to_dict
    user_dict = model_to_dict(user)
    comm_list = ['name', 'phone', 'gender', 'date_birth']
    comm_dict = dict()
    for comm in comm_list:
        if user_dict[comm] is None:
            comm_dict[comm] = text_user_profile.basic_data_menu[comm]
        else:
            if comm == 'gender':
                comm_dict[comm] = user_dict[comm]['symbol']
            elif comm == 'date_birth':
                comm_dict[comm] = user_dict[comm].strftime('%d.%m.%Y')
            else:
                comm_dict[comm] = user_dict[comm]
    for key, value in comm_dict.items():
        if value == prompt:
            kb = kb_user_profile.back_button()
            if key == 'phone':
                kb = kb_user_profile.choose_phone()
            elif key == 'gender':
                kb = kb_user_profile.choose_gender()
            await msg.answer(text=text_user_profile.basic_data_update[key],
                             reply_markup=kb)
            await state.set_state(text_user_profile.basic_data_states[key])
            break
    else:
        await msg.answer(text=text_navigator.err_command)
        await state.set_state(StateMenu.user_profile)


@router.message(StateUserProfile.phone)
async def user_profile_main(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    contact = msg.contact.phone_number
    if prompt == 'Отмена':
        await msg.answer(text='Ваши данные',
                         reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
        await state.set_state(StateMenu.user_profile)
        return
    else:
        if contact:
            corr_data = easy_funcs.correction_datas(phone_number=contact)
        else:
            corr_data = easy_funcs.correction_datas(phone_number=prompt)
        check_data = easy_funcs.checking_data_expression(phone_number=corr_data)
        if check_data:
            upd = db_funcs_user_account.user_update_data(user_id=user_id, column_datas='phone', data=corr_data)
            if upd:
                await msg.answer(text=text_user_profile.update_account_true,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            else:
                await msg.answer(text=text_user_profile.update_account_false,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            await state.set_state(StateMenu.user_profile)
        else:
            await msg.answer(text=text_user_profile.err_basic_data_update['phone'])


@router.message(StateUserProfile.name)
async def user_profile_main(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text='Ваши данные',
                         reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
        await state.set_state(StateMenu.user_profile)
    else:
        if len(prompt) < 64:
            upd = db_funcs_user_account.user_update_data(user_id=user_id, column_datas='name', data=prompt)
            if upd:
                await msg.answer(text=text_user_profile.update_account_true,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            else:
                await msg.answer(text=text_user_profile.update_account_false,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            await state.set_state(StateMenu.user_profile)
        else:
            await msg.answer(text=text_user_profile.err_basic_data_update['name'])


@router.message(StateUserProfile.date_birth)
async def user_profile_main(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text='Ваши данные',
                         reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
        await state.set_state(StateMenu.user_profile)
    else:
        corr_data = easy_funcs.correction_datas(date_day=prompt)
        check_data = easy_funcs.checking_data_expression(date_day=corr_data)
        if check_data:
            upd = db_funcs_user_account.user_update_data(user_id=user_id, column_datas='date_birth', data=corr_data)
            if upd:
                await msg.answer(text=text_user_profile.update_account_true,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            else:
                await msg.answer(text=text_user_profile.update_account_false,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            await state.set_state(StateMenu.user_profile)
        else:
            await msg.answer(text=text_user_profile.err_basic_data_update['date_birth'])


@router.message(StateUserProfile.gender)
async def user_profile_main(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == 'Отмена':
        await msg.answer(text='Ваши данные',
                         reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
        await state.set_state(StateMenu.user_profile)
    else:
        genders = Gender.select(Gender.symbol)
        check_data = [i.symbol for i in genders]
        if prompt in check_data:
            id = Gender.get(Gender.symbol == prompt)
            upd = db_funcs_user_account.user_update_data(user_id=user_id, column_datas='gender', data=id.id)
            if upd:
                await msg.answer(text=text_user_profile.update_account_true,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            else:
                await msg.answer(text=text_user_profile.update_account_false,
                                 reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
            await state.set_state(StateMenu.user_profile)
        else:
            await msg.answer(text=text_user_profile.err_basic_data_update['gender'])
