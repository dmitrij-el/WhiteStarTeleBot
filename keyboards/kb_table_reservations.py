from datetime import date, timedelta, datetime
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)

from data.models_peewee import data_tables


def date_enter(day_date: datetime = None, weeks_fnc: bool = False) -> ReplyKeyboardMarkup:
    date_enter_buttons = [[], []]
    if day_date is None:
        date_date = date.today()
    else:
        date_date = day_date
    for i in range(6):
        date_text = date_date.strftime('%d-%m-%Y %a')
        if i < 3:
            date_enter_buttons[0].append(KeyboardButton(text=date_text))
        else:
            date_enter_buttons[1].append(KeyboardButton(text=date_text))
        if weeks_fnc:
            date_date += timedelta(weeks=1)
        else:
            date_date += timedelta(days=1)
    date_enter_buttons.append([KeyboardButton(text="Отмена")])
    date_enter_keyboard = ReplyKeyboardMarkup(keyboard=date_enter_buttons,
                                              resize_keyboard=True,
                                              input_field_placeholder='Убедитесь в правильности ввода.')
    return date_enter_keyboard


def time_enter(day_date: datetime = None) -> ReplyKeyboardMarkup:
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
    num_line = (hour // 4)
    if hour % 4 > 0:
        num_line += 1
    time_enter_buttons = []
    for line in range(0, num_line):
        time_enter_buttons.append([])
        for i in range(4):
            time_text = str(start_hours % 24) + ':00'
            time_enter_buttons[line].append(KeyboardButton(text=time_text))
            start_hours += 1
            if start_hours == end_hours:
                break
    time_enter_buttons.append([KeyboardButton(text="Отмена"),
                               KeyboardButton(text="Назад")])
    time_enter_keyboard = ReplyKeyboardMarkup(keyboard=time_enter_buttons,
                                              resize_keyboard=True,
                                              input_field_placeholder='Убедитесь в правильности ввода.')
    return time_enter_keyboard


def yes_no() -> ReplyKeyboardMarkup:
    yes_no_buttons = [[KeyboardButton(text="Да"),
                       KeyboardButton(text="Нет")],
                      [KeyboardButton(text='Назад')]]
    yes_no_keyboard = ReplyKeyboardMarkup(keyboard=yes_no_buttons,
                                          resize_keyboard=True,
                                          input_field_placeholder='Выберите соответствующую кнопку.')
    return yes_no_keyboard


def choosing_a_free_table(table_list: list) -> ReplyKeyboardMarkup:
    free_tables_buttons = []
    if len(table_list) != 0:
        lines = ((len(table_list) + 1) // 4) + 1
        for i in range(lines):
            free_tables_buttons.append([])
        vip = False
        if 0 in table_list:
            len_table_list = len(table_list) - 1
        else:
            len_table_list = len(table_list)
        n = len_table_list // 2 + len_table_list % 2
        if n == 0:
            free_tables_buttons.append([KeyboardButton(text=data_tables['0']['symbol'])])
        else:
            for i in range(len(table_list)):
                line = i // n
                if vip:
                    line += 1
                print(line)
                kb = data_tables[str(table_list[i])]['symbol']
                print(table_list[i], type(table_list[i]))
                if table_list[i] == 0:
                    free_tables_buttons = [[KeyboardButton(text=kb)]] + free_tables_buttons
                    vip = True
                else:
                    free_tables_buttons[line].append(KeyboardButton(text=kb))
        free_tables_buttons.append([])
        free_tables_buttons[-1].append(KeyboardButton(text='Отмена'))
        free_tables_buttons[-1].append(KeyboardButton(text='Назад'))
    else:
        free_tables_buttons.append([KeyboardButton(text="Выбрать другое время")])

    free_tables_keyboard = ReplyKeyboardMarkup(keyboard=free_tables_buttons,
                                               resize_keyboard=True,
                                               input_field_placeholder='Выберите соответствующую кнопку.')
    return free_tables_keyboard


def number_of_seats(num_table: int) -> ReplyKeyboardMarkup:
    number_of_seats_buttons = []
    guests = data_tables[str(num_table)]['number_of_seats']
    lines = guests // 4 + 1
    for i in range(lines):
        number_of_seats_buttons.append([])
    for i in range(guests):
        if guests % 3 == 0:
            n = 3
        else:
            n = 4
        line = i // n
        number_of_seats_buttons[line].append(KeyboardButton(text=str(i + 1)))
    if guests % 4 == 0:
        number_of_seats_buttons.append([])
    number_of_seats_buttons.append([KeyboardButton(text='Отмена'),
                                    KeyboardButton(text='Назад')])
    number_of_seats_keyboard = ReplyKeyboardMarkup(keyboard=number_of_seats_buttons,
                                                   resize_keyboard=True,
                                                   input_field_placeholder='Выберите соответствующую кнопку.')
    return number_of_seats_keyboard
