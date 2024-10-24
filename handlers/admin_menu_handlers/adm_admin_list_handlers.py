from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.states import StateAdminMenu, StateMenu
from keyboards import kb_main_menu, kb_admin_menu
from data import db_funcs_admin_menu
from data.texts import text_admin_navigator
from data.db_funcs_user_account import check_admin
from data.models_peewee import db_beahea, Admin, User

router = Router()


@router.message(StateAdminMenu.admin_admin_list)
async def admin_events(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == "Добавить":
            await msg.answer(text=text_admin_navigator.admin_add_admin_list,
                             reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_add_admin_list)
        elif prompt == "Удалить":
            await msg.answer(text=text_admin_navigator.admin_delete_admin_list,
                             reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_delete_admin_list)
        elif prompt == 'Назад':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            await msg.answer(text=text_admin_navigator.err_admin_command,
                             reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
            await state.set_state(StateAdminMenu.admin_admin_list)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_add_admin_list)
async def admin_delete_events(msg: Message, state: FSMContext):
    def check_id(x):
        try:
            int(x)
            x = len(x) == 9
            return bool(x)
        except ValueError:
            return False

    def check_username(x):
        try:
            x = x[0] == '@'
            return bool(x)
        except ValueError:
            return False

    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            if True in [check_id(prompt), check_username(prompt)]:
                datas = dict()
                with db_beahea.atomic():
                    if check_id(prompt):
                        prompt = int(prompt)
                        datas['user_id'] = prompt
                        user = User.select().where(User.user_id == datas['user_id'])
                        if user:
                            datas['username'] = user.get().username
                    elif check_username(prompt):
                        datas['username'] = prompt[1::]
                        user = User.select().where(User.username == datas['username'])
                        if user:
                            datas['user_id'] = user.get().user_id
                    Admin.create(**datas)
                answer = await db_funcs_admin_menu.load_admin_list()
                for ans in answer:
                    await msg.answer(text=ans)
                await msg.answer(text=text_admin_navigator.admin_admin_list,
                                 reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_admin_list)
            else:
                await msg.answer(text=text_admin_navigator.err_error
                                      + text_admin_navigator.admin_add_admin_list,
                                 reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                await state.set_state(StateAdminMenu.admin_add_admin_list)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)


@router.message(StateAdminMenu.admin_delete_admin_list)
async def admin_delete_events(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    prompt = msg.text
    if check_admin(user_id=user_id):
        if prompt == 'Отмена':
            await msg.answer(text=text_admin_navigator.admin_main_menu,
                             reply_markup=kb_admin_menu.admin_main_menu(user_id=user_id))
            await state.clear()
            await state.set_state(StateAdminMenu.admin_main_menu)
        else:
            with db_beahea:
                check_date = Admin.select().where(Admin.id == int(prompt))
                if check_date:
                    check_date.get().delete_instance()
                    answer = await db_funcs_admin_menu.load_admin_list()
                    for ans in answer:
                        await msg.answer(text=ans)
                    await msg.answer(text=text_admin_navigator.admin_admin_list,
                                     reply_markup=kb_admin_menu.admin_party_reservations_menu(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_admin_list)
                else:
                    await msg.answer(text=text_admin_navigator.err_error
                                          + text_admin_navigator.admin_delete_admin_list,
                                     reply_markup=kb_admin_menu.admin_cancel(user_id=user_id))
                    await state.set_state(StateAdminMenu.admin_delete_admin_list)
    else:
        await msg.answer(text=text_admin_navigator.err_admin_access_rights,
                         reply_markup=kb_main_menu.main_menu(user_id=user_id))
        await state.set_state(StateMenu.main_menu)
