from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.states import StateMenu

router = Router()


@router.message(Command('start'))
async def reg_profile(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'start'. При вызове проверяет на наличие юзера.
    Если юзера нет записывает данные пользователя в БД.
    Если есть, предлагает обнулить данные.


    :param msg: Сообщение от пользователя
    :param state: Состояние бота

    """

    user_id = msg.from_user.id
    user = db_funcs.check_user_datas(user_id=user_id)
    if user:
        await db_funcs.rec_user_command(user_id=msg.from_user.id, command_text='start')
        await msg.answer(text.greet_cont.format(user_id=user_id),
                         reply_markup=kb_user_profile.ReplyKeyboardRemove()
                         )
        await msg.answer(text=text.account_qst_clear,
                         reply_markup=kb_user_profile.choice_delete_account(text.weather_menu))
        await state.set_state(StateUserProfile.clear_profile)

    else:
        acc_dict = {
            'user_id': msg.from_user.id,
            'name': msg.from_user.first_name,
            'surname': msg.from_user.last_name,
            'username': msg.from_user.username
        }
        db_funcs.user_rec_datas_in_reg(acc_dict)
        if db_funcs.check_user_datas(user_id):
            await db_funcs.rec_user_command(user_id=msg.from_user.id, command_text='start')
            await msg.answer(text.greet.format(name=msg.from_user.first_name))
            await msg.answer(text=text.greet_cont,
                             reply_markup=kb_user_profile.main_menu())
            await state.set_state(StateMenu.profile)
        else:
            await msg.answer('Произошла критическая ошибка при регистрации. Уведомите пожалуйста администратора.\n'
                             'Следующее сообщение будет отправлено администратору.')
            prompt = msg.text
            await msg.answer(text=prompt, reply_markup=kb_user_profile.main_menu())


@router.message(Command('main_menu'))
async def reg_profile(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'main_menu'. При вызове отправляет в главное меня.

    :param msg: Сообщение от пользователя
    :param state: Состояние бота
    """
    await db_funcs.rec_user_command(user_id=msg.from_user.id, command_text='main_menu')
    await msg.answer(text=text.command_found.format(command="main_menu"),
                     reply_markup=kb_user_profile.ReplyKeyboardRemove())
    await msg.answer(text=text.menu, reply_markup=kb_user_profile.main_menu())
    await state.set_state(StateGen.menu)


@router.message(Command('weather_menu'))
async def reg_profile(msg: Message, state: FSMContext):
    """
    Реагирует на команду 'weather_menu'. При вызове выводит меню прогноза погоды.

    :param msg: Сообщение от пользователя
    :param state: Состояние бота
    """
    await db_funcs.rec_user_command(user_id=msg.from_user.id, command_text='weather_menu')
    await msg.answer(text=text.command_found.format(command="weather_menu"))
    city_check = db_funcs.city_check_in_user(user_id=msg.from_user.id)
    if isinstance(city_check, str):
        weather_day = weather.request_weather_period_day(city=city_check)
        await msg.answer(text=text.weather_datas_day.format(**weather_day),
                         reply_markup=kb_weather.weather_main_menu(prompt=text.weather_menu,
                                                                   user_id=msg.from_user.id))
        await state.set_state(StateMenu.weather_menu)
    else:
        await msg.answer(text=text.weather_update_location,
                         reply_markup=kb_weather.weather_update_location(prompt=text.weather_update_location))
        await state.set_state(StateWeatherMenu.weather_city_now)


@router.message(Command('help'))
async def send_help(msg: Message):
    """
    Отправляет список команд для использования.

    :param msg: Сообщение от пользователя
    """
    await db_funcs.rec_user_command(user_id=msg.from_user.id, command_text='help')
    await msg.answer(text="Вот список команд для использования")
    await msg.answer(text="""
/start - Запуск бота. Автоматически создается аккаунт. При повторном вызове предлагает сбросить профиль.
/main_menu - Выводит главное меню.
/weather_menu - Выводит меню прогноза погоды.
/hello-world - Приветствие.
/help - Список команд
/history - Выводит историю команд.
""",
                     reply_markup=kb_user_profile.main_menu())


@router.message(Command('history'))
async def send_help(msg: Message, state: FSMContext):
    history_commands = models.UserHistoryCommands.select().where(models.UserHistoryCommands.user_id == msg.from_user.id)
    if history_commands:
        await msg.answer(text='Ваша история команд:', reply_markup=kb_user_profile.ReplyKeyboardRemove())
        history = history_commands
        for cmds in history:
            await msg.answer(text='Дата: {}\nКоманда: {}'.format(cmds.creation_time.strftime('%d.%m.%Y %H:%M:%S'),
                                                                 cmds.command.name))
    else:
        await msg.answer(text='Ваша история команд пуста', reply_markup=kb_user_profile.main_menu())
    await state.set_state(StateGen.menu)
