from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tele_bot.states.states import StateGen
from tele_bot.data import text, db_funcs
from tele_bot.keyboards import kb_user_profile


router = Router()


@router.message(F.text.lower().in_({"выйти в меню", "главное меню"}))
async def menu(msg: Message, state: FSMContext):
    await msg.answer(text=text.close_all_keyboards, reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text.menu, reply_markup=kb_user_profile.main_menu())
    await state.set_state(StateGen.menu)


@router.message(F.text.lower().in_({'Привет'.lower(), '/hello-world'}))
async def hello_hand(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'hellow-world'. Отправляет приветственное сообщение и
    возвращает в главное меню.

    :param msg: Сообщение от пользователя
    :param state: Состояние бота
    """
    await msg.answer(text='Хендлер из задания')
    await msg.answer(text=text.greet.format(name=msg.from_user.first_name),
                     reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text=text.menu,
                     reply_markup=kb_user_profile.main_menu())
    await state.set_state(StateGen.menu)


