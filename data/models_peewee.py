import datetime
import logging

from peewee import (CharField, DateTimeField, MySQLDatabase, TextField,
                    IntegerField, BooleanField, ForeignKeyField, FloatField)
from peewee import Model, InternalError, PrimaryKeyField

from config.config import DB_LOGIN, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

data_zona = [
    {'name_zona': 'VIP-Zona'},
    {'name_zona': 'Game-Zona'},
    {'name_zona': 'Bar-Zona'},
    {'name_zona': 'Well-Bar-Zona'},
    {'name_zona': 'Well-Rest-Zona'},
    {'name_zona': 'Center-Rest-Zona'},
    {'name_zona': 'BackAlley-Rest-Zona'}
]
data_gender = [
    {'name': 'men', 'symbol': '♂️'},
    {'name': 'women', 'symbol': '♀️'}]
data_tables = {
    '0': {'symbol': '⭐ᴠɪᴘ⭐', 'number_table': 0, 'name_table': 'Vip-комната', 'number_of_seats': 6, 'zona': 1, 'cor_x': 102, 'cor_y': 1511},
    '1': {'symbol': '①', 'number_table': 1, 'name_table': 'Стол №1', 'number_of_seats': 4, 'zona': 2, 'cor_x': 295, 'cor_y': 1520},
    '2': {'symbol': '②', 'number_table': 2, 'name_table': 'Стол №2', 'number_of_seats': 4, 'zona': 2, 'cor_x': 500, 'cor_y': 1413},
    '3': {'symbol': '③', 'number_table': 3, 'name_table': 'Стол №3', 'number_of_seats': 9, 'zona': 2, 'cor_x': 500, 'cor_y': 1508},
    '5': {'symbol': '⑤', 'number_table': 5, 'name_table': 'Стол №5', 'number_of_seats': 6, 'zona': 4, 'cor_x': 52, 'cor_y': 1285},
    '6': {'symbol': '⑥', 'number_table': 6, 'name_table': 'Стол №6', 'number_of_seats': 6, 'zona': 4, 'cor_x': 52, 'cor_y': 1083},
    '7': {'symbol': '⑦', 'number_table': 7, 'name_table': 'Стол №7', 'number_of_seats': 6, 'zona': 4, 'cor_x': 52, 'cor_y': 878},
    '8': {'symbol': '⑧', 'number_table': 8, 'name_table': 'Стол №8', 'number_of_seats': 6, 'zona': 5, 'cor_x': 52, 'cor_y': 512},
    '9': {'symbol': '⑨', 'number_table': 9, 'name_table': 'Стол №9', 'number_of_seats': 6, 'zona': 5, 'cor_x': 52, 'cor_y': 311},
    '10': {'symbol': '⑩', 'number_table': 10, 'name_table': 'Стол №10', 'number_of_seats': 6, 'zona': 5, 'cor_x': 52, 'cor_y': 106},
    '11': {'symbol': '⑪', 'number_table': 11, 'name_table': 'Стол №11', 'number_of_seats': 9, 'zona': 6, 'cor_x': 239, 'cor_y': 65},
    '12': {'symbol': '⑫', 'number_table': 12, 'name_table': 'Стол №12', 'number_of_seats': 6, 'zona': 7, 'cor_x': 489, 'cor_y': 54},
    '13': {'symbol': '⑬', 'number_table': 13, 'name_table': 'Стол №13', 'number_of_seats': 6, 'zona': 7, 'cor_x': 492, 'cor_y': 368},
    '14': {'symbol': '⑭', 'number_table': 14, 'name_table': 'Стол №14', 'number_of_seats': 6, 'zona': 7, 'cor_x': 218, 'cor_y': 312},
}



def create_models() -> None:
    """
    Создание БД
    :return: None
    """
    try:
        Gender.create_table()
        User.create_table()
        Admin.create_table()
        Zona.create_table()
        Event.create_table()
        Table.create_table()
        TableReservationHistory.create_table()
        PartyReservationHistory.create_table()

        with db_beahea.atomic():
            zona = Zona.select()
            if not zona:
                for data_dict in data_zona:
                    Zona.create(**data_dict)
            gender = Gender.select()
            if not gender:
                for data_dict in data_gender:
                    Gender.create(**data_dict)
            table = Table.select()
            if not table:
                for id, data_dict in data_tables.items():
                    Table.create(**data_dict)
    except InternalError as pw:
        logging.error(pw)


db_beahea = MySQLDatabase(DB_NAME,
                          user=DB_LOGIN,
                          password=DB_PASSWORD,
                          host=DB_HOST,
                          port=int(DB_PORT))


# db_beahea = SqliteDatabase('./db_db')


class BaseUserModel(Model):
    class Meta:
        database = db_beahea
        order_by = 'id'


class Gender(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(unique=True)
    symbol = CharField(unique=True)

    class Meta:
        db_table = "gender"


class User(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    user_id = CharField(unique=True)
    creation_time = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True, null=True)

    phone = CharField(null=True)
    name = CharField(max_length=63, null=True)
    gender = ForeignKeyField(Gender, null=True)
    date_birth = DateTimeField(null=True)
    username = CharField(max_length=63, null=True)

    class Meta:
        db_table = "user"


class Admin(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    user_id = CharField(null=True)
    username = CharField(null=True)

    class Meta:
        db_table = "admin"


class Event(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name_event = CharField(null=True)
    description_event = TextField(null=True)
    media_event = TextField(null=True)
    creation_time = DateTimeField(default=datetime.datetime.now)
    weekday = CharField(null=True)
    start_time_event = DateTimeField()
    end_time_event = DateTimeField()

    class Meta:
        db_table = "event"


class Zona(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name_zona = CharField()

    class Meta:
        db_table = "zona"


class Table(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    number_table = IntegerField()
    name_table = CharField(null=True)
    number_of_seats = IntegerField(null=True)
    zona = ForeignKeyField(Zona, backref='zona', null=True)
    cor_x = FloatField(null=True)
    cor_y = FloatField(null=True)

    class Meta:
        db_table = "table"


class TableReservationHistory(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    user = ForeignKeyField(User, backref='user', null=True)
    table = ForeignKeyField(Table, backref='table', null=True)
    event = ForeignKeyField(Event, backref='event', null=True)
    creation_time = DateTimeField(default=datetime.datetime.now())
    booking_start_time = DateTimeField(null=True)
    booking_end_time = DateTimeField(null=True)
    number_of_guests = IntegerField(null=True)
    phone_number = CharField(null=True)
    name_user = CharField(null=True)

    class Meta:
        db_table = 'table_reservation_history'


class PartyReservationHistory(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    user = ForeignKeyField(User, backref='user', null=True)
    tables_list = CharField(null=True)
    creation_time = DateTimeField(default=datetime.datetime.now())
    booking_start_time = DateTimeField(null=True)
    booking_end_time = DateTimeField(null=True)
    number_of_guests = IntegerField(null=True)
    phone_number = CharField(null=True)
    name_user = CharField(null=True)

    class Meta:
        db_table = 'party_reservation_history'


