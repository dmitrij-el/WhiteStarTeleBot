from data.models_peewee import User
from states.states import StateUserProfile


go_to_point_menu = 'В данном разделе хранятся все ваши данные. Для перехода выберите соответствующий пункт меню'
account_menu_1='Ваш профиль.',
account_menu_2='Для изменения нажмите на соответствующую кнопку.',
account_qst_clear='У вас уже есть профиль, хотите его очистить?',
account_rec_datas='Подождите, данные записываются.',
clear_account_question='Хотите сбросить профиль?',
clear_account_true='Аккаунт очищен.',
clear_account_wait='Идет удаление аккаунта...',
clear_account_cancel='Очистка аккаунта отменена.',
update_profile_wait='Идет обновление данных...',
update_account_true='Обновление данных прошло успешно.',
update_account_false='При обновлении данных произошла ошибка.',
update_profile_enter_data='Введите новые данные.'

basic_data_menu=dict(
    name='Имя',
    date_birth='Дата рождения',
    gender='Пол',
    phone='Телефон'
),
basic_data_datas=dict(
    name=User.name,
    date_birth=User.date_birth,
    gender=User.gender,
    phone=User.phone
),
basic_data_update=dict(
    name='Введите ваше имя.',
    date_birth='Введите дату рождения в формате ДД.ММ.ГГГГ или ДД/ММ/ГГГГ.',
    gender='Выберите ваш пол.',
    phone='Поделитесь своим контактом или введите номер телефона вручную.',
),
basic_data_states=dict(
    name=StateUserProfile.name,
    date_birth=StateUserProfile.date_birth,
    gender=StateUserProfile.gender,
    phone=StateUserProfile.phone,
),
err_basic_data_update=dict(
    name='Ошибка. Для имени можно использовать любой набор символов менее 64 букв.'
         + '\nЕсли вы считаете что ошибки нету, просим написать администратору в личку.',
    date_birth='Ошибка. Дата рождения в формате ДД.ММ.ГГГГ или ДД/ММ/ГГГГ.'
               + '\nЕсли вы считаете что ошибки нету, просим написать администратору в личку.',
    gender=('Ошибка. Для выбора пола воспользуйтесь кнопками ниже, или введите: '
            '\n"men" - мужской, '
            '\n"woman" - женский'
            + '\nЕсли вы считаете что ошибки нету, просим написать администратору в личку.'
            ),
    phone='Ошибка. Некорректный номер телефона'
          + '\nЕсли вы считаете что ошибки нету, просим написать администратору в личку.'
)
