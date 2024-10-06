from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.states import StateMenu, StateAdminMenu
from keyboards import kb_main_menu, kb_admin_menu
from data import db_funcs_user_account
from data.texts import text_navigator, text_admin_navigator
from data.db_funcs_user_account import check_admin

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
    user = db_funcs_user_account.check_user_datas(user_id=user_id)
    if user:
        await msg.answer(text=text_navigator.greet_cont_replay.format(name=msg.from_user.first_name),
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)

    else:
        acc_dict = {
            'user_id': msg.from_user.id,
            'name': msg.from_user.first_name,
            'surname': msg.from_user.last_name,
            'username': msg.from_user.username
        }
        db_funcs_user_account.user_rec_datas_in_reg(acc_dict=acc_dict)
        if db_funcs_user_account.check_user_datas(user_id):
            await msg.answer(text=text_navigator.greet_cont.format(name=msg.from_user.first_name),
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.set_state(StateMenu.main_menu)
        else:
            await msg.answer(text=text_navigator.err_reg_fatal)
            prompt = msg.text
            await msg.answer(text=prompt)
            await state.set_state(StateMenu.main_menu)


@router.message(Command('main_menu'))
@router.message(F.text.lower().in_({"выйти в меню", "главное меню", 'главное меню'}))
async def main_menu(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    await msg.answer(text=text_navigator.main_menu, reply_markup=kb_main_menu.main_menu(user_id=user_id))
    await state.set_state(StateMenu.main_menu)


@router.message(StateMenu.main_menu)
async def main_menu(msg: Message, state: FSMContext):
    prompt = msg.text
    if prompt == "Меню администратора":
        if check_admin(msg.from_user.id):
            await msg.answer(text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.adm_main_menu(user_id=msg.from_user.id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                             reply_markup=kb_main_menu.main_menu(user_id=user_id))
            await state.set_state(StateMenu.main_menu)


@router.message(Command('info_events'))
@router.message(F.text.lower().in_({"расписание мероприятий", "календарь", "расписание"}))
@router.message(F.text.in_({"🗓️ Расписание мероприятий"}))
async def info_events(msg: Message, state: FSMContext):
    await msg.answer(text='расписание мероприятий! надо проработать ответ',
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))


@router.message(Command('table_reservations'))
@router.message(F.text.lower().in_({"забронировать стол", "стол"}))
@router.message(F.text.in_({"⏸️ Забронировать стол"}))
async def table_reservations(msg: Message, state: FSMContext):
    await msg.answer(text='забронировать стол')


@router.message(Command('party_reservations'))
@router.message(F.text.lower().in_({"забронировать корпоратив", "корпоратив", "party", "вечеринка"}))
@router.message(F.text.in_({"⏸️ Забронировать корпоратив"}))
async def corporate_reservations(msg: Message, state: FSMContext):
    await msg.answer(text='company party')


@router.message(Command('info_rest'))
@router.message(F.text.lower().in_({"об whitestar", "whitestar"}))
@router.message(F.text.in_({"⭐ Об WhiteStar"}))
async def info_rest(msg: Message, state: FSMContext):
    await msg.answer(text='О white Star',
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))
    await msg.answer_location(latitude=55.889991, longitude=37.587959)
    await msg.answer(text='https://yandex.ru/maps/-/CDTf4UnL')


@router.message(Command('menu_rest'))
@router.message(F.text.lower().in_({"меню", "еда", "ресторанное меню"}))
async def menu_rest(msg: Message, state: FSMContext):
    await msg.answer(text="https://wslounge.ru/menu",
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))


@router.message(Command('profile'))
@router.message(F.text.lower().in_({"профиль"}),
                F.text.in_({"👤 Профиль"}))
async def user_profile(msg: Message, state: FSMContext):
    await msg.answer(text='Ваши данные',
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))


@router.message(Command('help'))
@router.message(F.text.lower().in_({"помощь", "help"}))
async def send_help(msg: Message, state: FSMContext):
    await msg.answer(text="Вот список команд для использования")
    await msg.answer(text="""
/start - Запуск бота.
/main_menu - Главное меню.
/info_events - Расписание мероприятий
/table_reservations - Забронировать стол
/party_reservations - Забронировать корпоратив
/menu_rest - Меню ресторана
/info_rest - Информация о ресторане.
/profile - Данные профиля
/help - Список команд
""",
                     reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))
    await state.set_state(StateMenu.main_menu)
