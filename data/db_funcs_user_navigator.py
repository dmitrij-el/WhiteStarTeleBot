from datetime import datetime

import logging

from data.texts import text_admin_navigator
from data.models_peewee import db_beahea
from data.models_peewee import TableReservationHistory, PartyReservationHistory, Event


async def load_events() -> list:
    try:
        with (db_beahea):
            datas = Event.select().where(Event.end_time_event.cast('date')
                                         >= datetime.now().date()
                                         ).order_by(Event.start_time_event)

            if datas:
                answer = []
                for data in datas:
                    answer.append('')
                    name_event = data.name_event
                    start_time_event = data.start_time_event
                    end_time_event = data.end_time_event
                    description_event = data.description_event
                    weekday = ', '.join([key for key, value
                                         in text_admin_navigator.weekday_dicts.items() for day
                                         in data.weekday.split(',') if value == int(day)])
                    answer[-1] += (f'\n\n<b><u>{name_event}</u></b>'
                                   f'\nДата старта мероприятия: {start_time_event}'
                                   f'\nДата конца мероприятия: {end_time_event}'
                                   f'\nДни недели, проведения мероприятия: {weekday}'
                                   f'\nОписание:\n{description_event}\n')
                if len(answer) != 0:
                    return answer
                else:
                    return [f'На данный момент активных мероприятий и акций не найдено.']
            else:
                return ['На данный момент активных мероприятий и акций не найдено.']
    except Exception as exp:
        logging.error(f'В процессе загрузки мероприятий произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return ['В процессе загрузки мероприятий произошла непредвиденная ошибка\n']


async def load_table_reservations(user_id: int) -> list | None:
    try:

        datas = TableReservationHistory.select().where(TableReservationHistory.user.user_id == user_id and
                                                       TableReservationHistory.booking_start_time.cast('date')
                                                       >= datetime.now().date()
                                                       ).order_by(TableReservationHistory.booking_start_time)
        if datas:
            answer = list()
            for data in datas:
                answer.append('')
                reserve_id = data.id
                table = data.table.number_table
                number_of_guests = data.number_of_guests
                phone = data.user.phone
                booking_start_time = data.booking_start_time.strftime('%d-%m-%Y %H:%M')
                answer[-1] += (f'\n\n<b><u>id резерва: {reserve_id}</u></b>'
                               f'\nНомер стола: {table}'
                               f'\nКоличество гостей: {number_of_guests}'
                               f'\nДата и время резерва: {booking_start_time}')
                answer[-1] += f'\nНомер телефона: {phone}'
            if len(answer) != 0:
                return answer
            else:
                return None
        else:
            return None
    except Exception as exp:
        logging.error(f'В процессе загрузки резервов столов произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return [f'В процессе загрузки резервов столов произошла непредвиденная ошибка\n']


async def load_party_reservations(user_id: int) -> list | None:
    try:

        datas = PartyReservationHistory.select().where(PartyReservationHistory.user.user_id == user_id and
                                                       PartyReservationHistory.booking_start_time.cast('date')
                                                       >= datetime.now().date()
                                                       ).order_by(PartyReservationHistory.booking_start_time)
        if datas:
            answer = list()
            for data in datas:
                answer.append('')
                reserve_id = data.id
                number_of_guests = data.number_of_guests
                phone = data.user.phone
                booking_start_time = data.booking_start_time.strftime('%d-%m-%Y %H:%M')
                answer[-1] += (f'\n\n<b><u>id резерва: {reserve_id}</u></b>'
                               f'\nКоличество гостей: {number_of_guests}'
                               f'\nДата и время резерва: {booking_start_time}')
                answer[-1] += f'\nНомер телефона: {phone}'
            if len(answer) != 0:
                return answer
            else:
                return None
        else:
            return None
    except Exception as exp:
        logging.error(f'В процессе загрузки резервов вечеринок произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return [f'В процессе загрузки вечеринок произошла непредвиденная ошибка\n']
