"""Набор функций для работы с базами данных"""

import logging
from data.models_peewee import db_beahea
from data.models_peewee import User, Admin
from config.config import ADMIN_DIMA


def check_user_datas(user_id: int) -> bool:
    """
    Проверка БД на наличие пользователя

    :param user_id: ID пользователя
    :return: True если юзера есть в БД, иначе False
    """
    try:
        with db_beahea:
            user = User.select().where(User.user_id == user_id)
            return bool(user)
    except Exception as exp:
        logging.error(f'В процессе проверки на наличие пользователя произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False


def user_rec_datas_in_reg(acc_dict: dict) -> None:
    """Запись данных профиля в БД при регистрации

    :param acc_dict: Данные профиля
    :return: None
    """
    try:
        with db_beahea.atomic():
            User.create(**acc_dict)
    except Exception as exp:
        logging.error(f'В процессе записи пользователя {acc_dict["user_id"]} в БД произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')


def user_delete_datas(user_id: int) -> bool:
    """Удаление данных пользователя из БД

    :param user_id: ID пользователя
    :return: True при удачном удалении, иначе False
    """
    try:
        with db_beahea:
            user = User.select().where(User.user_id == user_id).get()
            user.delete_instance()
    except Exception as exp:
        logging.error(f'В процессе удаления пользователя {user_id} произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False
    try:
        user = User.select().where(User.user_id == user_id).get()
        return bool(user)
    except Exception as exp:
        logging.error(exp)
        return True


def user_update_data(user_id: int, column_datas: str, data: str | int | bool) -> bool:
    """
    Функция обновления данных пользователя с фильтрами.

    :param user_id: ID пользователя
    :param column_datas: Имя обновляемой колонки
    :param data: Новые данные
    :return: True при удачном обновление, иначе False
    """
    try:
        with db_beahea:
            user = User.update({column_datas: data}).where(User.user_id == user_id)
            user.execute()
        return True
    except Exception as exp:
        logging.error(f'В процессе обновления данных пользователя {user_id} по ключу произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False


def check_admin(user_id: int = None):

    admin_list = list()
    admin_list.append(int(ADMIN_DIMA))
    with db_beahea:
        adm = Admin.select()
        for id_adm in adm:
            if id_adm.user_id is not None:
                admin_list.append(int(id_adm.user_id))
    return bool(user_id in admin_list)
