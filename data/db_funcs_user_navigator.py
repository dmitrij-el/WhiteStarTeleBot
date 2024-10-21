from datetime import datetime

import logging

from aiogram.utils.media_group import MediaGroupBuilder

from data.texts import text_admin_navigator
from data.models_peewee import db_beahea
from data.models_peewee import TableReservationHistory, PartyReservationHistory, Event, User


async def load_events() -> list | str:
    try:
        with (db_beahea):
            datas = Event.select().where(Event.end_time_event.cast('date')
                                         >= datetime.now().date()
                                         ).order_by(Event.start_time_event)
            if datas:
                answer_list = list()
                for data in datas:
                    caption = ''
                    name_event = data.name_event
                    description_event = data.description_event
                    start_time_event = data.start_time_event
                    end_time_event = data.end_time_event
                    start_time_event = start_time_event.strftime('%d %B')
                    end_time_event = end_time_event.strftime('%d %B')
                    if 'ь' in start_time_event:
                        start_time_event = start_time_event[:-1] + 'я'
                    elif 'т' in start_time_event:
                        start_time_event += 'а'
                    if 'ь' in end_time_event:
                        end_time_event = end_time_event[:-1] + 'я'
                    elif 'т' in end_time_event:
                        end_time_event += 'а'
                    weekday = ', '.join([key for key, value
                                         in text_admin_navigator.weekday_dicts.items() for day
                                         in data.weekday.split(',') if value == int(day)])
                    caption += (f'\n<u><b>{name_event}</b></u>'
                                f'\nС <b>{start_time_event}</b>'
                                f' по <b>{end_time_event}</b>'
                                f' по <b>{weekday}</b>'
                                f'\n<b>Описание:</b>\n{description_event}\n')
                    media_group = MediaGroupBuilder(caption=caption)
                    media_links = data.media_event.split(' // ')
                    for i in range(len(media_links)):
                        media_links[i] = media_links[i].split(' | ')
                    for media in media_links:
                        if media[1] == 'photo':
                            media_group.add_photo(type="photo", media=media[0])
                        elif media[1] == 'video':
                            media_group.add_video(type="video", media=media[0])
                        elif media[1] == 'document':
                            media_group.add(type="document", media=media[0])
                    answer_list.append(media_group)
                if len(answer_list) != 0:
                    return answer_list
                else:
                    return f'На данный момент активных мероприятий и акций не найдено.'
            else:
                return 'На данный момент активных мероприятий и акций не найдено.'
    except Exception as exp:
        logging.error(f'В процессе загрузки мероприятий произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return 'В процессе загрузки мероприятий произошла непредвиденная ошибка\n'


async def load_table_reservations(user_id: int) -> list | None:
    try:

        datas = TableReservationHistory.select().where(TableReservationHistory.user == User.get(user_id==user_id),
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
                booking_start_time = data.booking_start_time.strftime('%d-%m-%Y %H:%M')
                answer[-1] += (f'\n\n<b><u>id резерва: {reserve_id}</u></b>'
                               f'\nНомер стола: {table}'
                               f'\nКоличество гостей: {number_of_guests}'
                               f'\nДата и время резерва: {booking_start_time}')
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

        datas = PartyReservationHistory.select().where(PartyReservationHistory.user == User.get(user_id==user_id),
                                                       PartyReservationHistory.booking_start_time.cast('date')
                                                       >= datetime.now().date()
                                                       ).order_by(PartyReservationHistory.booking_start_time)
        if datas:
            answer = list()
            for data in datas:
                answer.append('')
                reserve_id = data.id
                number_of_guests = data.number_of_guests
                booking_start_time = data.booking_start_time.strftime('%d-%m-%Y %H:%M')
                answer[-1] += (f'\n\n<b><u>id резерва: {reserve_id}</u></b>'
                               f'\nКоличество гостей: {number_of_guests}'
                               f'\nДата и время резерва: {booking_start_time}')
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
