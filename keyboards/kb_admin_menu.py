from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)
from data.db_funcs_user_account import check_admin


def adm_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        menu_buttons = [
            [KeyboardButton(text="Добавить/удалить забронированные столы"),
             KeyboardButton(text="Добавить/удалить корпоративы")],
            [KeyboardButton(text="Добавить/удалить мероприятие"),
             KeyboardButton(text="Добавить/удалить администратора")],
            [KeyboardButton(text="Главное меню")]
        ]
    else:
        menu_buttons = [[KeyboardButton(text="Главное меню")]]
    menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons,
                                        resize_keyboard=True,
                                        input_field_placeholder='Выберите соответствующую кнопку.')
    return menu_keyboard



def adm_cancel(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_cancel_buttons = [[KeyboardButton(text="Отмена")]]
    else:
        adm_cancel_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_cancel_keyboard = ReplyKeyboardMarkup(keyboard=adm_cancel_buttons,
                                          resize_keyboard=True,
                                          input_field_placeholder='Очистить аккаунт?')
    return adm_cancel_keyboard


def adm_yes_no(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_yes_no_buttons = [[KeyboardButton(text="Да"),
                           KeyboardButton(text="Нет")]]
    else:
        adm_yes_no_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_yes_no_keyboard = ReplyKeyboardMarkup(keyboard=adm_yes_no_buttons,
                                          resize_keyboard=True,
                                          input_field_placeholder='Очистить аккаунт?')
    return adm_yes_no_keyboard


def adm_admin_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_admin_menu_buttons = [
            [KeyboardButton(text="Добавить администратора"),
             KeyboardButton(text="Удалить администратора")],
            [KeyboardButton(text="Назад")]
        ]
    else:
        adm_admin_menu_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_admin_menu_keyboard = ReplyKeyboardMarkup(keyboard=adm_admin_menu_buttons,
                                                  resize_keyboard=True,
                                                  input_field_placeholder='Выберите соответствующую кнопку.')
    return adm_admin_menu_keyboard


def adm_table_reservations_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_table_reservations_menu_buttons = [
            [KeyboardButton(text="Добавить бронь стола"),
             KeyboardButton(text="Удалить бронь стола")],
            [KeyboardButton(text="Назад")]
        ]
    else:
        adm_table_reservations_menu_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_table_reservations_menu_keyboard = ReplyKeyboardMarkup(keyboard=adm_table_reservations_menu_buttons,
                                                               resize_keyboard=True,
                                                               input_field_placeholder='Выберите соответствующую кнопку.')
    return adm_table_reservations_menu_keyboard


def adm_party_reservations_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_party_reservations_menu_buttons = [
            [KeyboardButton(text="Добавить бронь корпоратива"),
             KeyboardButton(text="Удалить бронь корпоратива")],
            [KeyboardButton(text="Назад")]
        ]
    else:
        adm_party_reservations_menu_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_party_reservations_menu_keyboard = ReplyKeyboardMarkup(keyboard=adm_party_reservations_menu_buttons,
                                                               resize_keyboard=True,
                                                               input_field_placeholder='Выберите соответствующую кнопку.')
    return adm_party_reservations_menu_keyboard


def adm_event_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_event_menu_buttons = [
            [KeyboardButton(text="Добавить мероприятие"),
             KeyboardButton(text="Удалить мероприятие")],
            [KeyboardButton(text="Назад")]
        ]
    else:
        adm_event_menu_buttons = [[KeyboardButton(text="Главное меню")]]

    adm_event_menu_keyboard = ReplyKeyboardMarkup(keyboard=adm_event_menu_buttons,
                                                  resize_keyboard=True,
                                                  input_field_placeholder='Выберите соответствующую кнопку.')
    return adm_event_menu_keyboard
