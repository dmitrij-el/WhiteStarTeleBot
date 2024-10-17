import asyncio
import json
from datetime import datetime

import logging
from playhouse.shortcuts import model_to_dict

from data.texts import text_admin_navigator
from data.models_peewee import db_beahea
from data.models_peewee import User, Admin, Table, TableReservationHistory, PartyReservationHistory, Event
from config.config import ADMIN_DIMA




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
                    id = data.id
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