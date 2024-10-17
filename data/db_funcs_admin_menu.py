from datetime import datetime

import logging

from data.texts import text_admin_navigator
from data.models_peewee import db_beahea
from data.models_peewee import User, Admin, TableReservationHistory, PartyReservationHistory, Event


async def load_table_reservations(date: datetime = None) -> list:
    try:
        with (db_beahea):
            if date:
                datas = TableReservationHistory.select().where(TableReservationHistory.booking_start_time.cast('date')
                                                               == date.date()
                                                               ).order_by(TableReservationHistory.booking_start_time)
            else:
                datas = TableReservationHistory.select().where(TableReservationHistory.booking_start_time.cast('date')
                                                               >= datetime.now().date()
                                                               ).order_by(TableReservationHistory.booking_start_time)
            if datas:
                answer = list()
                cont_day = datetime
                for data in datas:
                    user = data.user
                    reserve_id = data.id
                    table = data.table.number_table
                    number_of_guests = data.number_of_guests
                    booking_start_time = data.booking_start_time.strftime('%d-%m-%Y %H:%M')
                    if cont_day != data.booking_start_time.strftime('%d-%m-%Y %A'):
                        answer.append('')
                        cont_day = data.booking_start_time.strftime('%d-%m-%Y %A')
                        answer[-1] += f'\n\n<b><u>{cont_day}</u></b>'
                    answer[-1] += (f'\n\nid резерва: {reserve_id}'
                                   f'\nНомер стола: {table}'
                                   f'\nКоличество гостей: {number_of_guests}'
                                   f'\nДата и время резерва: {booking_start_time}')
                    if data.phone_number:
                        phone = data.phone_number
                    else:
                        phone = data.user.phone
                    answer[-1] += f'\nНомер телефона: {phone}'
                    if data.name_user:
                        name_guest = data.name_user
                        answer[-1] += f'\nИмя: {name_guest}'
                    if user:
                        answer[-1] += f'\nДанные о {user.name}: @{user.username}'
                        gender = user.gender
                        date_birth = user.date_birth
                        if gender is not None:
                            answer[-1] += f', {user.gender.symbol}'
                        if date_birth is not None:
                            date_birth = date_birth.date()
                            answer[-1] += f', {date_birth}'
                if len(answer) != 0:
                    return answer
                else:
                    return ['Зарезервированных столов не найдено.']
            else:
                return [f'Зарезервированных столов не найдено.']
    except Exception as exp:
        logging.error(f'В процессе загрузки резервов столов произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return [f'В процессе загрузки резервов столов произошла непредвиденная ошибка\n']


async def load_party_reservations(date: datetime = None) -> list:
    try:
        with (db_beahea):
            if date:
                datas = PartyReservationHistory.select().where(PartyReservationHistory.booking_start_time.cast('date')
                                                               == date.date()
                                                               ).order_by(PartyReservationHistory.booking_start_time)
            else:
                datas = PartyReservationHistory.select().where(PartyReservationHistory.booking_start_time.cast('date')
                                                               >= datetime.now().date()
                                                               ).order_by(PartyReservationHistory.booking_start_time)
            if datas:
                answer = list()
                cont_day = datetime
                for data in datas:
                    user = data.user
                    reserve_id = data.id
                    number_of_guests = data.number_of_guests
                    booking_start_time = data.booking_start_time.strftime('%d-%m-%Y %H:%M')
                    name_guest = data.name_user
                    if cont_day != data.booking_start_time.strftime('%d-%m-%Y %A'):
                        cont_day = data.booking_start_time.strftime('%d-%m-%Y %A')
                        answer.append('')
                        answer[-1] += f'\n\n<b><u>{cont_day}</u></b>'
                    answer[-1] += (f'\n\nid резерва: {reserve_id}'
                                   f'\nКоличество гостей: {number_of_guests}'
                                   f'\nДата и время резерва: {booking_start_time}')
                    if data.phone_number:
                        phone = data.phone_number
                    else:
                        phone = data.user.phone
                    answer[-1] += f'\nНомер телефона: {phone}'
                    if name_guest:
                        answer[-1] += f'\nИмя: {name_guest}'
                    if user:
                        answer[-1] += f'\nДанные о {user.name}: @{user.username}'
                        gender = user.gender
                        date_birth = user.date_birth
                        if gender is not None:
                            answer[-1] += f', {user.gender.symbol}'
                        if date_birth is not None:
                            date_birth = date_birth.date()
                            answer[-1] += f', {date_birth}'
                if len(answer) != 0:
                    return answer
                else:
                    return [f'Зарезервированных корпоративов не найдено.']
            else:
                return [f'Зарезервированных корпоративов не найдено.']
    except Exception as exp:
        logging.error(f'В процессе загрузки резервов корпоративов произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return ['В процессе загрузки резервов корпоративов произошла непредвиденная ошибка\n']


async def load_events(date: datetime = None) -> list:
    try:
        with (db_beahea):
            if date:
                datas = Event.select().where(Event.start_time_event.cast('date')
                                             <= date.date() <=
                                             Event.end_time_event
                                             ).order_by(Event.start_time_event).cast('date')
            else:
                datas = Event.select().where(Event.end_time_event.cast('date')
                                             >= datetime.now().date()
                                             ).order_by(Event.start_time_event)

            if datas:
                answer = []
                for data in datas:
                    answer.append('')
                    event_id = data.id
                    name_event = data.name_event
                    start_time_event = data.start_time_event
                    end_time_event = data.end_time_event
                    description_event = data.description_event
                    weekday = ', '.join([key for key, value
                                         in text_admin_navigator.weekday_dicts.items() for day
                                         in data.weekday.split(',') if value == int(day)])
                    answer[-1] += (f'\n\nid мероприятия: {event_id}'
                                   f'\nНазвание мероприятия: {name_event}'
                                   f'\nДата старта мероприятия: {start_time_event}'
                                   f'\nДата конца мероприятия: {end_time_event}'
                                   f'\nДни недели, проведения мероприятия: {weekday}'
                                   f'\nОписание:\n{description_event}\n')
                if len(answer) != 0:
                    return answer
                else:
                    return [f'Мероприятий не найдено.']
            else:
                return ['Мероприятий не найдено.']
    except Exception as exp:
        logging.error(f'В процессе загрузки мероприятий произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return ['В процессе загрузки мероприятий произошла непредвиденная ошибка\n']


async def load_admin_list():
    try:
        datas = Admin.select()
        if datas:
            answer = []
            for data in datas:
                answer.append('')
                admin_id = data.id
                user_id = data.user_id
                answer[-1] += f'ID записи: {admin_id}'
                answer[-1] += f'\nID пользователя: {user_id}'
                user = User.select().where(User.user_id == user_id)
                if user:
                    user = user.get()
                    answer[-1] += f'\nДанные о {user.name}'
                    answer[-1] += f'\nНик: @{user.username}'
                    gender = user.gender
                    date_birth = user.date_birth
                    phone = user.phone
                    if phone is not None:
                        answer[-1] += f'\nТелефон: {phone}'
                    if gender is not None:
                        answer[-1] += f'\nПол: {user.gender.symbol}'
                    if date_birth is not None:
                        date_birth = date_birth.date()
                        answer[-1] += f'\nДень рождения: {date_birth}'
            if len(answer) != 0:
                return answer
            else:
                return ['Администраторов не найдено.']
        else:
            return ['Администраторов не найдено.']
    except Exception as exp:
        logging.error(f'В процессе загрузки списка администраторов произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return ['В процессе загрузки списка администраторов произошла непредвиденная ошибка\n']