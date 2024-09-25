"""Набор функций для работы с базами данных"""

import logging
from typing import Coroutine, Any

from aiogram.fsm.context import FSMContext
from data.models_peewee import db_beahea
from data.models_peewee import (BaseUserModel, User, UserProfileBasicData, UserProfileTrain,
                                UserProfileGoals, UserProfileQuestionnaire, UserProfileLimitsFactors)


def check_user_datas(user_id: int) -> bool:
    """Проверка БД на наличие пользователя

    :param user_id: ID пользователя
    :return: True если юзера есть в БД, иначе False
    """
    try:
        with db_beahea:
            user = User.select().where(User.user_id == user_id).get()
            return bool(user)
    except Exception as exp:
        logging.error(f'В процессе проверки на наличие пользователя произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False


def user_get_data(user_id: int, name_data: str) -> BaseUserModel:
    """Подкачка данных пользователя из БД по ключу"""
    try:
        dict_requests = {'user_profile_basic_data': UserProfileBasicData.select().where(user_id == user_id),
                         'user_profile_questionnaire_questions': UserProfileQuestionnaire.select().where(user_id == user_id),
                         'the_goals_questions': UserProfileGoals.select().where(user_id == user_id),
                         'the_trane_questions': UserProfileTrain.select().where(user_id == user_id),
                         'the_limits_factors': UserProfileLimitsFactors.select().where(user_id == user_id)}
        if name_data in list(dict_requests.keys()):
            with db_beahea:
                user_datas = dict_requests[name_data].get()
                return user_datas
        else:
            raise logging.error(f'Не найден ключ запроса в данных. Юзер {user_id}')
    except Exception as exp:
        logging.error(f'В процессе загрузки данных {name_data} пользователя {user_id} произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')

def user_rec_datas_in_reg(user_id:int, acc_dict: dict) -> None:
    """Запись данных профиля в БД при регистрации

    :param user_id: user id
    :param acc_dict: Данные профиля
    :return: None
    """
    try:
        with db_beahea.atomic():
            User.create(user_id=user_id)
            UserProfileBasicData.create(**acc_dict)
    except Exception as exp:
        logging.error(f'В процессе записи пользователя {user_id} в БД произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')


def user_delete_datas(user_id: int) -> bool:
    """Удаление данных пользователя из БД

    :param user_id: ID пользователя
    :return: True при удачном удалении, иначе False
    """
    try:
        with db_beahea:
            user = UserProfileBasicData.select().where(User.user_id == user_id).get()
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

            user = UserProfileBasicData.update({column_datas: data}).where(UserProfileBasicData.user_id == user_id)
            user.execute()
        return True
    except Exception as exp:
        logging.error(f'В процессе обновления данных пользователя {user_id} по ключу произошла непредвиденная ошибка\n'
                      f'Ошибка: {exp}')
        return False


def check_user_profile_questions(user_id: int, question: str) -> bool:
    """Проверка БД на наличие ответов на вопросы в анкете пользователя

    :param user_id: ID пользователя
    :param question: вопрос пользователю
    :return: True если ответ есть в БД, иначе False
    """
    try:
        with db_beahea:
            answer = UserProfileQuestionnaire.select().where(User.user_id == user_id)
            return bool(answer.get())
    except Exception as exp:
        logging.error(f'В процессе проверки на наличие {question} произошла ошибка\n'
                      f'Ошибка: {exp}')
        return False