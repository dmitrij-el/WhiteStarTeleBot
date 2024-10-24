from datetime import date, timedelta, datetime
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)
from data.db_funcs_user_account import check_admin


def admin_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        menu_buttons = [
            [KeyboardButton(text="Резервы столов"),
             KeyboardButton(text="Резервы корпоративов")],
            [KeyboardButton(text="Мероприятия"),
             KeyboardButton(text="Администраторы")],
            [KeyboardButton(text="Главное меню")]
        ]
    else:
        menu_buttons = [[KeyboardButton(text="Главное меню")]]
    menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons,
                                        resize_keyboard=True,
                                        input_field_placeholder='Выберите соответствующую кнопку.')
    return menu_keyboard


def admin_cancel(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_cancel_buttons = [[KeyboardButton(text="Отмена")]]
    else:
        adm_cancel_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_cancel_keyboard = ReplyKeyboardMarkup(keyboard=adm_cancel_buttons,
                                              resize_keyboard=True,
                                              input_field_placeholder='Убедитесь в правильности ввода.')
    return adm_cancel_keyboard


def admin_load_or_cancel(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        admin_load_or_cancel_buttons = [[KeyboardButton(text="Загрузить"),
                                         KeyboardButton(text="Отмена")]]
    else:
        admin_load_or_cancel_buttons = [[KeyboardButton(text="Главное меню")]]
    admin_load_or_cancel_keyboard = ReplyKeyboardMarkup(keyboard=admin_load_or_cancel_buttons,
                                                        resize_keyboard=True,
                                                        input_field_placeholder='Убедитесь в правильности ввода.')
    return admin_load_or_cancel_keyboard


def admin_yes_no(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_yes_no_buttons = [[KeyboardButton(text="Да"),
                               KeyboardButton(text="Нет")]]
    else:
        adm_yes_no_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_yes_no_keyboard = ReplyKeyboardMarkup(keyboard=adm_yes_no_buttons,
                                              resize_keyboard=True,
                                              input_field_placeholder='Выберите соответствующую кнопку.')
    return adm_yes_no_keyboard


def admin_table_reservations_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_table_reservations_menu_buttons = [
            [KeyboardButton(text="Добавить"),
             KeyboardButton(text="Удалить")],
            [KeyboardButton(text="Список на день"),
             KeyboardButton(text="Назад")]
        ]
    else:
        adm_table_reservations_menu_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_table_reservations_menu_keyboard = ReplyKeyboardMarkup(keyboard=adm_table_reservations_menu_buttons,
                                                               resize_keyboard=True,
                                                               input_field_placeholder='Выберите соответствующую '
                                                                                       'кнопку.')
    return adm_table_reservations_menu_keyboard


def admin_party_reservations_menu(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        adm_party_reservations_menu_buttons = [
            [KeyboardButton(text="Добавить"),
             KeyboardButton(text="Удалить")],
            [KeyboardButton(text="Назад")]
        ]
    else:
        adm_party_reservations_menu_buttons = [[KeyboardButton(text="Главное меню")]]
    adm_party_reservations_menu_keyboard = ReplyKeyboardMarkup(keyboard=adm_party_reservations_menu_buttons,
                                                               resize_keyboard=True,
                                                               input_field_placeholder='Выберите соответствующую '
                                                                                       'кнопку.')
    return adm_party_reservations_menu_keyboard


def admin_date_enter(user_id: int, day_date: datetime = None, weeks_fnc: bool = False) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        admin_date_enter_buttons = [[], []]
        if day_date is None:
            date_date = date.today()
        else:
            date_date = day_date
        for i in range(6):
            date_text = date_date.strftime('%d-%m-%Y %a')
            if i < 3:
                admin_date_enter_buttons[0].append(KeyboardButton(text=date_text))
            else:
                admin_date_enter_buttons[1].append(KeyboardButton(text=date_text))
            if weeks_fnc:
                date_date += timedelta(weeks=1)
            else:
                date_date += timedelta(days=1)
        admin_date_enter_buttons.append([KeyboardButton(text="Отмена")])
    else:
        admin_date_enter_buttons = [[KeyboardButton(text="Главное меню")]]
    admin_date_enter_keyboard = ReplyKeyboardMarkup(keyboard=admin_date_enter_buttons,
                                                    resize_keyboard=True,
                                                    input_field_placeholder='Убедитесь в правильности ввода.')
    return admin_date_enter_keyboard


def admin_weekday_enter(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        admin_weekday_enter_buttons = [
            [KeyboardButton(text="Пн"),
             KeyboardButton(text="Вт"),
             KeyboardButton(text="Ср"),
             KeyboardButton(text="Чт")],
            [KeyboardButton(text="Пт"),
             KeyboardButton(text="Сб"),
             KeyboardButton(text="Вс")],
            [KeyboardButton(text="Будни"),
             KeyboardButton(text="Вся неделя")],
            [KeyboardButton(text="Подтвердить"),
             KeyboardButton(text="Отмена")]
        ]
    else:
        admin_weekday_enter_buttons = [[KeyboardButton(text="Главное меню")]]
    admin_weekday_enter_keyboard = ReplyKeyboardMarkup(keyboard=admin_weekday_enter_buttons,
                                                       resize_keyboard=True,
                                                       input_field_placeholder='Выберите соответствующую '
                                                                               'кнопку.')
    return admin_weekday_enter_keyboard


def admin_time_enter(user_id: int, day_date: datetime = None) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        if day_date.date() == datetime.now().date():
            start_hours = int(datetime.now().time().strftime("%H")) + 1
            if start_hours < 14:
                start_hours = 14
        else:
            start_hours = 14
        if day_date.weekday() in [4, 5]:
            end_hours = 30
        else:
            end_hours = 26
        hour = end_hours - start_hours
        print(hour)
        num_line = (hour // 4)
        print(num_line)
        if hour % 4 > 0:
            num_line += 1
        print(num_line)
        admin_time_enter_buttons = []
        for line in range(0, num_line):
            print(line)
            admin_time_enter_buttons.append([])
            for i in range(4):
                time_text = str(start_hours % 24) + ':00'
                admin_time_enter_buttons[line].append(KeyboardButton(text=time_text))
                start_hours += 1
                if start_hours == end_hours:
                    break
        admin_time_enter_buttons.append([KeyboardButton(text="Отмена")])
    else:
        admin_time_enter_buttons = [[KeyboardButton(text="Главное меню")]]
    admin_time_enter_keyboard = ReplyKeyboardMarkup(keyboard=admin_time_enter_buttons,
                                                    resize_keyboard=True,
                                                    input_field_placeholder='Убедитесь в правильности ввода.')
    return admin_time_enter_keyboard


def admin_add_media_event(user_id: int) -> ReplyKeyboardMarkup:
    if check_admin(user_id=user_id):
        admin_add_media_event_buttons = [
            [KeyboardButton(text="Далее")],
            [KeyboardButton(text="Назад")]
        ]
    else:
        admin_add_media_event_buttons = [[KeyboardButton(text="Главное меню")]]
    admin_add_media_event_keyboard = ReplyKeyboardMarkup(keyboard=admin_add_media_event_buttons,
                                                         resize_keyboard=True,
                                                         input_field_placeholder='Выберите соответствующую '
                                                                                 'кнопку.')
    return admin_add_media_event_keyboard
