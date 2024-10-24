from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from data.models_peewee import User, Admin
from states.states import StateMenu, StateAdminMenu, StateTableReservations, StatePartyReservations
from keyboards import kb_main_menu, kb_admin_menu, kb_user_profile, kb_table_reservations
from data import db_funcs_user_account, db_funcs_user_navigator
from data.texts import text_navigator, text_admin_navigator, text_reservation, text_user_profile
from data.db_funcs_user_account import check_admin
from config.config import ADMIN_DIMA

router = Router()


@router.message(CommandStart())
async def handler_start(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'start'. При вызове проверяет на наличие юзера.
    Если юзера нет записывает данные пользователя в БД.
    Если есть, предлагает обнулить данные.


    :param msg: Сообщение от пользователя
    :param state: Состояние бота

    """

    user_id = msg.from_user.id
    username = msg.from_user.username
    surname = msg.from_user.last_name
    name = msg.from_user.first_name
    user = db_funcs_user_account.check_user_datas(user_id=user_id)
    if user:
        await msg.answer(text=text_navigator.greet_cont_replay.format(name=msg.from_user.first_name),
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)

    else:
        acc_dict = {
            'user_id': user_id,
            'name': name,
            'surname': surname,
            'username': username
        }
        db_funcs_user_account.user_rec_datas_in_reg(acc_dict=acc_dict)
        if db_funcs_user_account.check_user_datas(user_id):
            check_admin_user_user_id = Admin.select().where(Admin.user_id == user_id)
            check_admin_user_username = Admin.select().where(Admin.username == username)
            if check_admin_user_user_id:
                check_admin_user = check_admin_user_user_id.get()
                check_admin_username = check_admin_user.username
                if check_admin_username is None:
                    adm = Admin.update(username = username).where(Admin.user_id == user_id)
                    adm.execute()
            elif check_admin_user_username:
                check_admin_user = check_admin_user_username.get()
                check_admin_user_id = check_admin_user.user_id
                if check_admin_user_id is None:
                    adm = Admin.update(user_id = user_id).where(Admin.username == username)
                    adm.execute()
            await msg.answer(text=text_navigator.greet_cont.format(name=name),
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.set_state(StateMenu.main_menu)
        else:
            await msg.answer(text=text_navigator.err_reg_fatal)
            prompt = msg.text
            await msg.send_message(chat_id=ADMIN_DIMA, text=prompt)


@router.message(Command('main_menu'))
@router.message(F.text.lower().in_({"выйти в меню", 'главное меню'}))
async def f_main_menu(msg: Message, state: FSMContext):
    await state.clear()
    user_id = msg.from_user.id
    await msg.answer(text=text_navigator.main_menu, reply_markup=kb_main_menu.main_menu(user_id=user_id))
    await state.set_state(StateMenu.main_menu)


@router.message(StateMenu.main_menu)
async def main_menu(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if prompt == "Меню администратора":
        if check_admin(msg.from_user.id):
            await msg.answer(text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.set_state(StateMenu.main_menu)


async def info_events(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    answer = await db_funcs_user_navigator.load_events()
    if type(answer) is str:
        await msg.answer(text=answer,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))

    else:
        for ans in answer:
            await msg.answer_media_group(media=ans.build(), reply_markup=kb_main_menu.main_menu(user_id=user_id))
    await state.set_state(StateMenu.main_menu)


async def table_reservations(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user = User.get(User.user_id == user_id)
    if user.phone is None:
        await msg.answer(
            text=text_reservation.add_table_reservations_phone + '\n' + text_user_profile.basic_data_update['phone'],
            reply_markup=kb_user_profile.choose_phone())
        await state.set_state(StateTableReservations.add_table_reservations_phone)
    else:
        answer = await db_funcs_user_navigator.load_table_reservations(user_id=user_id)
        if answer is not None:
            for ans in answer:
                await msg.answer(text=ans)
        await msg.answer(text=text_reservation.add_table_reservations_booking_start_time_date,
                         reply_markup=kb_table_reservations.date_enter())
        await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_date)


async def party_reservations(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user = User.get(User.user_id == user_id)
    if user.phone is None:
        await msg.answer(
            text=text_reservation.add_party_reservations_phone + '\n' + text_user_profile.basic_data_update['phone'],
            reply_markup=kb_user_profile.choose_phone())
        await state.set_state(StatePartyReservations.add_party_reservations_phone)
    else:
        answer = await db_funcs_user_navigator.load_party_reservations(user_id=user_id)
        if answer is not None:
            for ans in answer:
                await msg.answer(text=ans)
        await msg.answer(text=text_reservation.add_party_reservations_booking_start_time_date,
                         reply_markup=kb_table_reservations.date_enter())
        await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_date)


async def info_rest(msg: Message):
    await msg.answer(text='О white Star',
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))
    await msg.answer_location(latitude=55.889991, longitude=37.587959)
    await msg.answer(text='https://yandex.ru/maps/-/CDTf4UnL')


async def menu_rest(msg: Message):
    await msg.answer(text="https://wslounge.ru/menu",
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))


async def user_profile(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    await msg.answer(text='Ваши данные',
                     reply_markup=kb_user_profile.user_profile_basic_data(user_id=user_id))
    await state.set_state(StateMenu.user_profile)


async def send_help(msg: Message, state: FSMContext):
    await msg.answer(text="Вот список команд для использования")
    await msg.answer(text="""
/start - Запуск бота.
/main_menu - Главное меню.
/info_events - Расписание мероприятий.
/table_reservations - Забронировать стол.
/party_reservations - Забронировать корпоратив.
/menu_rest - Меню ресторана.
/info_rest - Информация о ресторане.
/profile - Данные профиля.
/help - Список команд.
""",
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))
    await state.set_state(StateMenu.main_menu)
