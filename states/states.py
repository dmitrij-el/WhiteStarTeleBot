from aiogram.fsm.state import StatesGroup, State

"""
Стадии взаимодействия с ботом.

"""


class StateMenu(StatesGroup):
    main_menu = State()
    table_reservations = State()
    info_events = State()
    user_profile = State()
    info_rest = State()
    admin_menu = State()
    help = State()


class StateTableReservations(StatesGroup):
    main_table_reservations = State()


class StateInfoEvents(StatesGroup):
    main_info_events = State()


class StateUserProfile(StatesGroup):
    name = State()
    date_birth = State()
    gender = State()
    phone = State()
    clear_profile = State()


class StateAdminMenu(StatesGroup):
    main_admin_menu = State()
