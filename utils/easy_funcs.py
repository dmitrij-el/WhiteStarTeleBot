import re

from aiogram.utils.media_group import MediaGroupBuilder

from data.models_peewee import User
from data.texts import text_admin_navigator


def checking_data_expression(phone_number: str | bool = False,
                             email: str | bool = False,
                             time: str | bool = False,
                             date_day: str | bool = False,
                             number_of_guests: str | bool = False) -> bool:
    """
    Проверка данных с помощью регулярных выражений. Выберите переменную из списка\n
    Номера телефона: phone_number\n
    Адреса электронной почты: email\n
    Имени пользователя: user_name

    :param number_of_guests: Количество гостей
    :param date_day: Дата
    :param time: Время
    :param phone_number: Номер телефона пользователя
    :param email: Адрес электронной почты пользователя

    :return: Сравнивает и возвращает True или False
    """

    expressions_dir = {
        'date':
            r'(19|20)\d\d[- /.,;:](0[1-9]|1[012])[- /.,;:](0[1-9]|[12][0-9]|3[01])',
        'time':
            r'^([0-1]?[0-9]|2[0-3])[:;.-/, ][0-5][0-9]',
        'number_of_guests':
            r'[0-9]?[0-9]',
        'phone_number':
            r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
        'email':
            r'^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$',
        'number_credit_card':
            r'[0-9]{13,16}'
    }
    expression = ''
    data = ''

    if phone_number:
        expression = expressions_dir["phone_number"]
        data = phone_number
    elif email:
        expression = expressions_dir["email"]
        data = email
    elif time:
        expression = expressions_dir["time"]
        data = time
    elif date_day:
        expression = expressions_dir["date"]
        data = date_day
    elif number_of_guests:
        expression = expressions_dir["number_of_guests"]
        data = number_of_guests

    pattern = re.compile(expression)
    res = pattern.search(str(data))
    if res:
        return True
    else:
        return False


def correction_datas(phone_number: str = None,
                     date_day: str = None,
                     time: str = None) -> str:
    if phone_number:
        ans = ''.join(re.findall(r'\b\d+\b', phone_number))
        if ans[0] == '7':
            ans = '+' + ans
        elif ans[0] == '8':
            ans = '+7' + ans.lstrip('8')
        elif ans[0] == '9':
            ans = '+7' + ans
        return ans
    elif date_day:
        ans = (re.findall(r'\b\d+\b', date_day))
        if len(ans[-1]) > len(ans[0]):
            ans[0], ans[-1] = ans[-1], ans[0]
        ans = '-'.join(ans)
        return ans
    elif time:
        ans = ':'.join(re.findall(r'\b\d+\b', time))
        return ans


def admin_checking_table_reservations(datas: dict) -> tuple[bool, str]:
    answer = text_admin_navigator.admin_add_table_reservations_confirmation_enter_data
    answer += (f'\nНомер стола: {datas['table']}'
               f'\nКоличество гостей: {datas['number_of_guests']}'
               f'\nДата и время резерва: {datas['booking_start_time']}'
               f'\nТелефон: {datas['phone_number']}')
    if datas.setdefault('name_user') is not None:
        answer += f'\nИмя: {datas['name_user']}'
    user = User.select().where(User.phone == datas['phone_number'])
    if user:
        user = user.get()
        answer += f'\nДанные о {user.name}: @{user.username}'
        gender = user.gender
        date_birth = user.date_birth
        if gender is not None:
            answer += f', {user.gender.symbol}'
        if date_birth is not None:
            date_birth = date_birth.date()
            answer += f', {date_birth}'
        return True, answer
    else:
        return False, answer


def admin_checking_party_reservations(datas: dict) -> tuple[bool, str]:
    answer = text_admin_navigator.admin_add_party_reservations_confirmation_enter_data
    answer += (f'\nКорпоратив'
               f'\nКоличество гостей: {datas['number_of_guests']}'
               f'\nДата и время резерва: {datas['booking_start_time']}'
               f'\nТелефон: {datas['phone_number']}')
    if datas.setdefault('name_user') is not None:
        answer += f'\nИмя: {datas['name_user']}'
    user = User.select().where(User.phone == datas['phone_number'])
    if user:
        user = user.get()
        answer += f'\nДанные о {user.name}: @{user.username}'
        gender = user.gender
        date_birth = user.date_birth
        if gender is not None:
            answer += f', {user.gender.symbol}'
        if date_birth is not None:
            date_birth = date_birth.date()
            answer += f', {date_birth}'
        return True, answer
    else:
        return False, answer


def admin_checking_event(datas: dict) -> MediaGroupBuilder:
    answer = ''
    weekday = ', '.join([key for key, value
                         in text_admin_navigator.weekday_dicts.items() for day
                         in datas['weekday'] if value == int(day)])
    answer += (f'\nНазвание мероприятия: <b>{datas['name_event']}</b>'
               f'\nДата старта мероприятия: <b>{datas['start_time_event']}</b>'
               f'\nДата конца мероприятия: <b>{datas['end_time_event']}</b>'
               f'\nДни недели, проведения мероприятия: <b>{weekday}</b>'
               f'\n<b>Описание:</b>\n{datas['description_event']}\n')
    media_group = MediaGroupBuilder(caption=answer)
    media_links = datas['media_event']
    for media in media_links:
        if media[1] == 'photo':
            media_group.add_photo(media=media[0])
        elif media[1] == 'video':
            media_group.add_video(media=media[0])
        elif media[1] == 'document':
            media_group.add_document(media=media[0])

    return media_group