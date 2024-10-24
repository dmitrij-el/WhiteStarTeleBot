"""
Для удобства работы с ботом реализуется клавиатура.

Интерфейс главного меню.
Интерфейс навигации по профилю

"""

import logging

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)

from data.texts import text_user_profile
from data.models_peewee import Gender, User, db_beahea


def choice_delete_account(prompt) -> ReplyKeyboardMarkup:
    choice_delete_account_buttons = [[KeyboardButton(text="Да"),
                                      KeyboardButton(text="Нет")]]
    choice_delete_account_keyboard = ReplyKeyboardMarkup(keyboard=choice_delete_account_buttons,
                                                         resize_keyboard=True,
                                                         input_field_placeholder=prompt)
    return choice_delete_account_keyboard


def user_profile_basic_data(user_id: int) -> ReplyKeyboardMarkup:
    """
    Клавиатура меню "Основных данных" пользователя.

    :param user_id: ID пользователя
    :return: Клавиатура с данными
    """
    profile_basic_data = User.select().where(User.user_id == user_id)
    if profile_basic_data is None:
        logging.error(f'Не найдет профиль {user_id}')
        user_profile_buttons = [
            [KeyboardButton(text="Что-то пошло не так, аккаунт не найден")]]
    else:
        user = User.get(User.user_id == user_id)
        from playhouse.shortcuts import model_to_dict
        user_datas = model_to_dict(user)
        user_profile_buttons = [[], [], []]
        for key in user_datas.keys():
            if user_datas[key] is None:
                user_datas[key] = text_user_profile.basic_data_menu[key]
            else:
                if key == 'gender':
                    user_datas[key] = user_datas[key]['symbol']
                elif key == 'date_birth':
                    user_datas[key] = user_datas[key].strftime('%d.%m.%Y')
        for key, value in user_datas.items():
            if key in ['name', 'phone']:
                user_profile_buttons[0].append(KeyboardButton(text=user_datas[key]))
            elif key in ['date_birth', 'gender']:
                user_profile_buttons[1].append(KeyboardButton(text=user_datas[key]))
        user_profile_buttons[2] = [KeyboardButton(text="Главное меню")]
    user_profile_keyboard = ReplyKeyboardMarkup(keyboard=user_profile_buttons,
                                                resize_keyboard=True,
                                                input_field_placeholder='Выберите соответствующую кнопку.')
    return user_profile_keyboard


def back_button() -> ReplyKeyboardMarkup:
    back_button_buttons = [[KeyboardButton(text="Отмена")]]
    back_button_keyboard = ReplyKeyboardMarkup(keyboard=back_button_buttons,
                                               resize_keyboard=True)
    return back_button_keyboard


def choose_phone() -> ReplyKeyboardMarkup:
    choose_phone_buttons = [[KeyboardButton(text="📞 Отправить телефон", request_contact=True),
                             KeyboardButton(text='Отмена')]]
    choose_phone_keyboard = ReplyKeyboardMarkup(keyboard=choose_phone_buttons,
                                                resize_keyboard=True)
    return choose_phone_keyboard


def choose_gender() -> ReplyKeyboardMarkup:
    button_gender = [[]]
    with db_beahea:
        genders = Gender.select()
        for gender in genders:
            button_gender[0].append(KeyboardButton(text=gender.symbol))
    button_gender.append([KeyboardButton(text='Отмена')])

    button_gender_keyboard = ReplyKeyboardMarkup(keyboard=button_gender,
                                                 resize_keyboard=True
                                                 )
    return button_gender_keyboard
