from aiogram.fsm.state import StatesGroup, State

"""
Стадии взаимодействия с ботом.

"""


class StateMenu(StatesGroup):
    main_menu = State()
    table_reservations = State()
    party_reservations = State()
    info_events = State()
    user_profile = State()
    info_rest = State()
    menu_rest = State()
    help = State()


class StateAdminMenu(StatesGroup):
    admin_main_menu = State()

    admin_table_reservations = State()
    admin_add_table_reservations_phone = State()
    admin_add_table_reservations_table = State()
    admin_add_table_reservations_booking_start_time_date = State()
    admin_add_table_reservations_booking_start_time_time = State()
    admin_add_table_reservations_number_of_guests = State()
    admin_add_table_reservations_confirmation_enter_data = State()
    admin_delete_table_reservations = State()

    admin_party_reservations = State()
    admin_add_party_reservations = State()
    admin_add_party_reservations_booking_start_time_date = State()
    admin_add_party_reservations_booking_start_time_time = State()
    admin_add_party_reservations_number_of_guests = State()
    admin_delete_party_reservations = State()

    admin_events = State()
    admin_add_events = State()
    admin_delete_events = State()

    admin_admin_list = State()
    admin_add_admin_list = State()
    admin_delete_admin_list = State()


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


