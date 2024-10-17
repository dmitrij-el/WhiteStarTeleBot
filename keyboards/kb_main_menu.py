"""
Для удобства работы с ботом реализуется клавиатура.

Интерфейс главного меню.
Интерфейс навигации по профилю

"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup
)

from data.db_funcs_user_account import check_admin


def main_menu(user_id) -> ReplyKeyboardMarkup:
    menu_buttons = [
        [KeyboardButton(text="Забронировать стол"),
         KeyboardButton(text="Забронировать корпоратив")],
        [KeyboardButton(text="Расписание мероприятий"),
         KeyboardButton(text="Меню")],
        [KeyboardButton(text="Об WhiteStar"),
         KeyboardButton(text="Профиль")]
    ]
    if check_admin(user_id=user_id):
        menu_buttons.append([KeyboardButton(text="Меню администратора")])
    menu_keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons,
                                        resize_keyboard=True,
                                        input_field_placeholder='Выберите соответствующую кнопку.')
    return menu_keyboard


def choice_delete_account() -> ReplyKeyboardMarkup:
    choice_delete_account_buttons = [[KeyboardButton(text="Да"),
                                      KeyboardButton(text="Нет")]]
    choice_delete_account_keyboard = ReplyKeyboardMarkup(keyboard=choice_delete_account_buttons,
                                                         resize_keyboard=True,
                                                         input_field_placeholder='Очистить аккаунт?')
    return choice_delete_account_keyboard


def back_button() -> ReplyKeyboardMarkup:
    back_button_buttons = [[KeyboardButton(text="Отмена")]]
    back_button_keyboard = ReplyKeyboardMarkup(keyboard=back_button_buttons,
                                               resize_keyboard=True)
    return back_button_keyboard


def choose_phone() -> ReplyKeyboardMarkup:
    back_button_buttons = [[KeyboardButton(text="Поделиться номером", request_contact=True),
                            KeyboardButton(text="Отмена")]]
    back_button_keyboard = ReplyKeyboardMarkup(keyboard=back_button_buttons,
                                               resize_keyboard=True)
    return back_button_keyboard


    # elif prompt == "Забронировать стол":
    #     if user.phone is None:
    #         await msg.answer(
    #             text=text_reservation.add_table_reservations_phone + '\n' +  text_user_profile.basic_data_update['phone'],
    #             reply_markup=kb_user_profile.choose_phone())
    #         await state.set_state(StateTableReservations.add_table_reservations_phone)
    #     else:
    #         await msg.answer(text=text_reservation.add_party_reservations_booking_start_time_date,
    #                          reply_markup=kb_table_reservations.date_enter())
    #         await state.set_state(StateTableReservations.add_table_reservations_booking_start_time_date)
    # elif prompt == "Забронировать корпоратив":
    #     if user.phone is None:
    #         await msg.answer(
    #             text=text_reservation.add_party_reservations_phone + '\n' + text_user_profile.basic_data_update['phone'],
    #             reply_markup=kb_user_profile.choose_phone())
    #         await state.set_state(StatePartyReservations.add_party_reservations_phone)
    #     else:
    #         await msg.answer(text=text_reservation.add_party_reservations_booking_start_time_date,
    #                          reply_markup=kb_table_reservations.date_enter())
    #         await state.set_state(StatePartyReservations.add_party_reservations_booking_start_time_date)
    # elif prompt == "Расписание мероприятий":
    #     user_id = msg.from_user.id
    #     answer = await db_funcs_user_navigator.load_events()
    #     for ans in answer:
    #         await msg.answer(text=ans)
    #     await msg.answer(text=text_navigator.main_menu,
    #                      reply_markup=kb_main_menu.main_menu(user_id=user_id))
    #     await state.set_state(StateMenu.main_menu)
    # elif prompt == "Меню":
    #     await msg.answer(text="https://wslounge.ru/menu",
    #                      reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))
    # elif prompt == "Об WhiteStar":
    #     await msg.answer(text='О white Star',
    #                      reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))
    #     await msg.answer_location(latitude=55.889991, longitude=37.587959)
    #     await msg.answer(text='https://yandex.ru/maps/-/CDTf4UnL')
    # elif prompt == "Профиль":
    #     await msg.answer(text='Ваши данные',
    #                      reply_markup=kb_main_menu.main_menu(user_id=msg.from_user.id))