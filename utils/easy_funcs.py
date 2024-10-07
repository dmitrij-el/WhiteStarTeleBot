import re

from data import models_peewee
from data.models_peewee import Gender
from data.texts import text_user_profile, text_admin_navigator


def text_buttons_profile(user_data: models_peewee.BaseUserModel) -> dict:
    """
    Функция для формирования текстового интерфейса клавиатуры в меню профиля

    :param user_data: Вводные данные из базы данных
    :return: Текстовый интерфейс клавиатуры в меню
    """

    user_data_dict = user_data.__dict__['__data__']
    pass


def check_data_func(key: str | int, mess: str) -> [bool, str]:
    """
    Функция проверки ввода данных аккаунта

    :param key: Название метода проверки
    
    :param mess: Текстовое сообщение для проверки на соответствие

    :return: Объект с информацией о результате проверки
    """
    if key in ['name', 'surname']:
        if len(mess) > 63:
            return (False,
                    text_user_profile.err_basic_data_update[key])
    elif key == 'date_birth':
        return (checking_data_expression(date=mess),
                text_user_profile.err_basic_data_update[key])
    elif key == 'phone':
        return (checking_data_expression(phone_number=mess),
                text_user_profile.err_basic_data_update[key])
    elif key == 'gender':
        ans_list = [[i.name, i.symbol] for i in Gender.select(Gender.name, Gender.symbol)]
        answer_list = []
        for ans in ans_list:
            for i in ans:
                answer_list.append(i)
        if not mess.title() in answer_list:
            return (False,
                    text_user_profile.err_basic_data_update[key])
    return True, text_user_profile.update_account_true


def checking_data_expression(phone_number: str | bool = False,
                             email: str | bool = False,
                             time: str | bool = False,
                             date: str | bool = False,
                             number_of_guests: str | bool = False) -> bool:
    """
    Проверка данных с помощью регулярных выражений. Выберите переменную из списка\n
    Номера телефона: phone_number\n
    Адреса электронной почты: email\n
    Имени пользователя: user_name

    :param number_of_guests: Количество гостей
    :param date: Дата
    :param time: Время
    :param phone_number: Номер телефона пользователя
    :param email: Адрес электронной почты пользователя

    :return: Сравнивает и возвращает True или False
    """

    expressions_dir = {
        'date':
            r'(0[1-9]|[12][0-9]|3[01])[- /.,;:](0[1-9]|1[012])[- /.,;:](19|20)\d\d',
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
    elif date:
        expression = expressions_dir["date"]
        data = date
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
                     date: str = None,
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
    elif date:
        ans = (re.findall(r'\b\d+\b', date))
        if len(ans[-1]) > len(ans[0]):
            ans[0], ans[-1] = ans[-1], ans[0]
        ans = '-'.join(ans)
        return ans
    elif time:
        ans = ':'.join(re.findall(r'\b\d+\b', time))
        return ans


def admin_checking_table_reservations(datas: dict) -> str:
    answer = text_admin_navigator.admin_add_party_reservations_confirmation_enter_data
    answer += (f'\nНомер стола: {datas['table']}\n'
               f'Количество гостей: {datas['number_of_guests']}\n'
               f'Дата и время резерва: {datas['booking_start_time']}\n'
               f'Телефон: {datas['phone_number']}\n\n')
    return answer
