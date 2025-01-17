# WhiteStar TelegramBot

![Star](https://github.com/dmitrij-el/WhiteStarTeleBot/tree/master/data/images/star.png)

### For SerGey from Dmitriy Ivanyuk 🤪😇
### 🤖 Бот разработан для 🌟WhiteStar Алтуфьево🌟.

## Общие сведения.
Работает в асинхронном режиме с помощью библиотеки *asyncio*.

Я использовал библиотеку *aiogram* как основную для работы бота.
Бот взаимодействует через конечные автоматы. Последнее состояние пользователя хранится 
Интерфейс был реализован посредством **ReplyKeyboard**:

### [Переменные окружения.](./config/.env)

| Команда     | Тип данных | Описание                     |
|-------------|------------|------------------------------|
| BOT_TOKEN   | str        | Токен-ключ от телеграм бота. |
| DB_LOGIN    | str        | Логин от базы данных MySQL   |
| DB_PASSWORD | str        | Пароль от БД                 |
| DB_NAME     | str        | Имя БД                       |
| DB_HOST     | str        | Адрес БД                     |
| DB_PORT     | int        | Порт БД                      |


### О работе бота
#### Хранит у себя данные пользователя.
По средствам библиотеки PeeWee бот формирует базу данных пользователей MySQL.
Пользователи могут менять о себе любую информацию, кроме:
1. id (выдается автоматически)
2. user_id - id Telegram
3. is_active - активность юзера.


### Команды выполняемые ботом.
#### Везде
| Команда              | Описание                                      |
|----------------------|-----------------------------------------------|
| /start	              | Запуск бота. Автоматически создается аккаунт. |
| /main_menu           | Вывод главного меню.                          |
| /info_events         | Расписание мероприятий.                       |
| /table_reservations	 | Забронировать стол.                           |
| /party_reservations	 | Забронировать корпоратив.                     |
| /menu_rest	          | Меню ресторана.                               |
| /info_rest	          | Информация о ресторане.                       |
| /profile             | Данные профиля.                               |
| /help                | Список команд.                                |
|


### Особенности
1. Имя токена BOT_TOKEN.
2. Токен должен лежать => [Конфигурационном файле переменных окружения](./config/.env).
3. Cостояния пользователя хранятся в базе данных SQLite [fsm.db](./data).
4. Включено игнорирование обработки сообщений если бот был выключен.
5. Включен Router для хранения кода в разных директориях и файлах, чтобы легче было его поддерживать.
6. Включено логирование. Все логи хранятся в корневой директории в py_log.log


## Зависимости
Эта программа зависит от интерпретатора Python версии 3.7 или выше.
У вас должны быть установлены [зависимости проекта](requirements.txt)


## Структура проекта

### WhiteStarTeleBot
| Директория/файл            | Описание                                                            |
|----------------------------|---------------------------------------------------------------------|
| [config](#config)          | Все, что связано с путями на сторонние ресурсы, ключами и токенами. |
| [data](#data)              | Файлы и данные. Все БД и все, что с ними связано .                  |
| [handlers](#handlers)      | Обработчики. Реакции бота на сообщения и команды.                   |
| [keyboards](#keyboards)    | Клавиатуры, кнопки.                                                 |
| [states](#states)          | Состояния пользователя.                                             |
| [utils](#utils)            | Функциональность бота                                               |
| [bot_main.py](bot_main.py) | Загрузочный файл                                                    |



### config
| Директория/файл               | Описание                                                                                                                 |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| .env                          | В данном файле должны лежать все ключи и токены для безопасности                                                         |
| .env.template                 | Шаблон переменных окружения                                                                                              |
| [config.py](config/config.py) | Для хранения всех url-ссылок сторонних ресурсов и переменные окружения, к которым можно обратиться за ключами и токенами |

### data
| Директория/файл                                               | Описание                                                |
|---------------------------------------------------------------|---------------------------------------------------------|
| [images](data/images)                                         | Необходимые картинки.                                   |
| [text](#text)                                                 | Текстовые ответы бота.                                  |                                                        |
| [db_funcs_admin_menu.py](data/db_funcs_admin_menu.py)         | Функции для работы с администраторскими запросами в БД. |
| [db_funcs_user_account.py](data/db_funcs_user_account.py)     | Функции для работы с профилем пользователя в БД.        |
| [db_funcs_user_navigator.py](data/db_funcs_user_navigator.py) | Функции для работы с пользовательскими запросами в БД.  |
| [models.py](data/models_peewee.py)                            | Модели объектов БД.                                     ||
| fsm.db                                                        | БД SQLite для хранения состояний пользователя.          |

### handlers
| Директория/файл                                                           | Описание                                                  |
|---------------------------------------------------------------------------|-----------------------------------------------------------|
| [admin_menu_handlers](#admin_menu_handlers)                               | Дериктория с обработчиками администраторских команд.      |
| [main_menu_handlers.py](handlers/main_menu_handlers.py)                   | Пользовательские обработчики в главном меню.              |
| [party_reservations_handlers.py](handlers/party_reservations_handlers.py) | Пользовательские обработчики резервирования корпоративов. |
| [table_reservations_handlers.py](handlers/table_reservations_handlers.py) | Пользовательские обработчики резервирования столов        |
| [user_profile_handlers.py](handlers/user_profile_handlers.py)             | Пользовательские обработчики данных профиля               |

### admin_menu_handlers
| Директория/файл                                                                                       | Описание                                                  |
|-------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [adm_admin_list_handlers.py](handlers/admin_menu_handlers/adm_admin_list_handlers.py)                 | Дериктория с обработчиками администраторских команд.      |
| [adm_events_handlers.py](handlers/admin_menu_handlers/adm_events_handlers.py)                         | Пользовательские обработчики в главном меню.              |
| [adm_main_menu_handlers.py](handlers/admin_menu_handlers/adm_main_menu_handlers.py)                   | Пользовательские обработчики резервирования корпоративов. |
| [adm_party_reservations_handlers.py](handlers/admin_menu_handlers/adm_party_reservations_handlers.py) | Пользовательские обработчики резервирования столов        |
| [adm_table_reservations_handlers.py](handlers/admin_menu_handlers/adm_table_reservations_handlers.py) | Пользовательские обработчики данных профиля               |

### keyboards
| Директория/файл                                                | Описание                     |
|----------------------------------------------------------------|------------------------------|
| [kb_admin_menu.py](keyboards/kb_admin_menu.py)                 | Администраторский интерфейс. |
| [kb_main_menu.py](keyboards/kb_main_menu.py)                   | Главное меню.                |
| [kb_table_reservations.py](keyboards/kb_table_reservations.py) | Резервирование.              |
| [kb_user_profile.py](keyboards/kb_user_profile.py)             | Интерфейс профиля пользователя. |

### text
| Директория/файл                                               | Описание                                    |
|---------------------------------------------------------------|---------------------------------------------|
| [text_admin_navigator.py](data/texts/text_admin_navigator.py) | Администраторский текстовый интерфейс.      |
| [text_navigator.py](data/texts/text_navigator.py)             | Интерфейс текстовой навигации пользователя. |
| [text_reservation.py](data/texts/text_reservation.py)         | Интерфейс текстовый для резервирования.     |
| [text_user_profile.py](data/texts/text_user_profile.py)       | Интерфейс текстовый профиля пользователя.   |

### states
| Директория/файл               | Описание                           |
|-------------------------------|------------------------------------|
| [states.py](states/states.py) | Состояния пользователя.            |

### utils
| Директория/файл                      | Описание                                                                |
|--------------------------------------|-------------------------------------------------------------------------|
| [easy_funcs.py](utils/easy_funcs.py) | Небольшие функции для обработки данных.                                 |


