"""
Для удобства работы с ботом реализуется клавиатура.

Интерфейс главного меню.
Интерфейс навигации по профилю

"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)

from data.db_funcs_user_account import check_admin


def main_menu(user_id) -> ReplyKeyboardMarkup:
    menu_buttons = [
        [KeyboardButton(text="⏸️ Забронировать стол"),
         KeyboardButton(text="⏸️ Забронировать корпоратив")],
        [KeyboardButton(text="🗓️ Расписание мероприятий"),
         KeyboardButton(text="Меню")],
        [KeyboardButton(text="⭐ Об WhiteStar"),
         KeyboardButton(text="👤 Профиль")]
    ]
    if check_admin(user_id=user_id):
        menu_buttons.append([KeyboardButton(text="Меню администратора")])
    menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons,
                                        resize_keyboard=True,
                                        input_field_placeholder='Выберите соответствующую кнопку.')
    return menu_keyboard


def choice_delete_account() -> ReplyKeyboardMarkup:
    choice_delete_account_buttons = [[KeyboardButton(text="Да"),
                                      KeyboardButton(text="Нет")]]
    choice_delete_account_keyboard = ReplyKeyboardMarkup(keyboard=choice_delete_account_buttons,
                                                         resize_keyboard=True,
                                                         input_field_placeholder='Очистить аккаунт?')
    return choice_delete_account_keyboard


def back_button() -> ReplyKeyboardMarkup:
    back_button_buttons = [[KeyboardButton(text="Отмена")]]
    back_button_keyboard = ReplyKeyboardMarkup(keyboard=back_button_buttons,
                                               resize_keyboard=True)
    return back_button_keyboard


def choose_phone() -> ReplyKeyboardMarkup:
    back_button_buttons = [[KeyboardButton(text="Поделиться номером", request_contact=True),
                            KeyboardButton(text="Отмена")]]
    back_button_keyboard = ReplyKeyboardMarkup(keyboard=back_button_buttons,
                                               resize_keyboard=True)
    return back_button_keyboard
