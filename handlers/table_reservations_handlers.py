from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.states import StateMenu, StateTableReservations
from keyboards import kb_main_menu
from data import db_funcs_user_account
from data.texts import text_navigator, text_event

router = Router()


@router.message(StateTableReservations.main_table_reservations)
async def menu(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    await msg.answer(text_navigator.main_menu, reply_markup=kb_main_menu.main_menu(user_id=user_id))
    await state.set_state(StateMenu.main_menu)

