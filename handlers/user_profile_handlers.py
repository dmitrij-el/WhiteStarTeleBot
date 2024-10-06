from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.states import StateAdminMenu, StateMenu
from keyboards import kb_main_menu, kb_admin_menu
from data import db_funcs_user_account, db_funcs_table_reservations
from data.texts import text_navigator, text_admin_navigator
from data.db_funcs_user_account import check_admin
from data.models_peewee import TableReservationHistory, Table, PartyReservationHistory, Event, Admin
from utils import easy_funcs

router = Router()
