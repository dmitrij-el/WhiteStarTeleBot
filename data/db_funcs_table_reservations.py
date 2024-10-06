"""Набор функций для работы с базами данных"""
import asyncio
from datetime import datetime

import logging
from playhouse.shortcuts import model_to_dict

from data.models_peewee import db_beahea
from data.models_peewee import User, Admin, Table, TableReservationHistory
from config.config import ADMIN_DIMA


def load_table_reservations(date: datetime = None) -> str:
    try:
        with (db_beahea):
            if date:
                datas = TableReservationHistory.select().where(TableReservationHistory.booking_start_time
                                                               == date.date()
                                                               ).order_by(TableReservationHistory.booking_start_time)
            else:
                datas = TableReservationHistory.select().where(TableReservationHistory.booking_start_time.cast('date')
                                                               >= datetime.now().date()
                                                               ).order_by(TableReservationHistory.booking_start_time)
            if datas:
                answer = ''
                for data in datas:
                    id = data.id
                    table = data.table.number_table
                    number_of_guests = data.number_of_guests
                    booking_start_time = data.booking_start_time.strftime('%d-%m-%Y %H:%M')
                    if data.phone_number:
                        phone = data.phone_number
                    else:
                        phone = data.user.phone
                    answer += (f'id резерва: {id}\n'
                               f'Номер стола: {table}\n'
                               f'Количество гостей: {number_of_guests}\n'
                               f'Дата и время резерва: {booking_start_time}\n'
                               f'Телефон: {phone}\n\n')
                return str(answer)
            else:
                return f'Зарезервированных столов не найдено.'
    except Exception as exp:
        logging.error(f'В процессе загрузки резервов столов произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return f'В процессе загрузки резервов столов произошла непредвиденная ошибка\nОшибка: {exp}'

