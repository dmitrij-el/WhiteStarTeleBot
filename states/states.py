from aiogram.fsm.state import StatesGroup, State


"""
Стадии взаимодействия с ботом.

"""



class StateMenu(StatesGroup):
    weather_menu = State()
    translator = State()
    profile = State()







class StateUserProfile(StatesGroup):
    change_name = State()
    change_date_birth = State()
    change_gender = State()
    change_phone = State()
    change_communication_channels = State()
    clear_profile = State()




