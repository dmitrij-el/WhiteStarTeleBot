from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.states import StateMenu
from keyboards import kb_main_menu
from data import db_funcs_user_account
from data.texts import text_navigator, text_event

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
        await msg.answer(text=text_navigator.greet_cont.format(user_id=user_id),
                         reply_markup=kb_main_menu.main_menu())
        await state.set_state(StateMenu.main_menu)

    else:
        acc_dict = {
            'user_id': msg.from_user.id,
            'name': msg.from_user.first_name,
            'surname': msg.from_user.last_name,
            'username': msg.from_user.username
        }
        db_funcs_user_account.user_rec_datas_in_reg(user_id=user_id, acc_dict=acc_dict)
        if db_funcs_user_account.check_user_datas(user_id):
            await msg.answer(text=text_navigator.greet_cont.format(user_id=user_id),
                             reply_markup=kb_main_menu.main_menu())
        else:
            await msg.answer(text=text_navigator.err_reg_fatal)
            prompt = msg.text
            await msg.answer(text=prompt, reply_markup=kb_main_menu.main_menu())
    await state.set_state(StateMenu.main_menu)


@router.message(F.text.lower().in_({"выйти в меню", "главное меню"}),
                F.state == StateMenu.main_menu,
                Command == 'menu')
async def menu(msg: Message, state: FSMContext):
    await msg.answer(text_navigator.main_menu, reply_markup=kb_main_menu.main_menu())
    await state.set_state(StateMenu.main_menu)


@router.message(F.text.lower().in_({"расписание мероприятий"}),
                F.state == StateMenu.info_events,
                Command == 'info_events')
async def hello_hand(msg: Message, state: FSMContext):
    await msg.answer(text='расписание мероприятий! надо проработать ответ',
                     reply_markup=kb_main_menu.main_menu())
    await state.set_state(StateMenu.main_menu)


@router.message(F.text.lower().in_({"забронировать стол"}),
                F.state == StateMenu.table_reservations,
                Command == 'table_reservations')
async def hello_hand(msg: Message, state: FSMContext):
    await msg.answer(text='расписание мероприятий! надо проработать ответ',
                     reply_markup=kb_main_menu.main_menu())
    await state.set_state(StateMenu.main_menu)


@router.message(F.text.lower().in_({"информация"}),
                F.state == StateMenu.info_rest,
                Command == 'info_rest')
async def hello_hand(msg: Message, state: FSMContext):
    await msg.answer(text='расписание мероприятий! надо проработать ответ',
                     reply_markup=kb_main_menu.main_menu())
    await state.set_state(StateMenu.main_menu)


@router.message(F.text.lower().in_({"помощь", "help"}),
                F.state == StateMenu.help,
                Command('help'))
async def send_help(msg: Message):
    await msg.answer(text="Вот список команд для использования")
    await msg.answer(text="""
/start - Запуск бота. Автоматически создается аккаунт. При повторном вызове предлагает сбросить профиль.
/menu - Выводит главное меню.
/info_events - 
/info_rest - 
/table_reservations - 
/info_rest - Выводит меню прогноза погоды.
/help - Список команд
""",
                     reply_markup=kb_main_menu.main_menu())
