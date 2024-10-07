import datetime
import logging

from peewee import (CharField, DateTimeField, MySQLDatabase,
                    IntegerField, BooleanField, ForeignKeyField, SqliteDatabase)
from peewee import Model, InternalError, PrimaryKeyField

from config.config import DB_LOGIN, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


def create_models() -> None:
    """
    Создание БД
    :return: None
    """
    try:

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
        data_tables = [
            {'number_table': 1},
        ]

        Gender.create_table()
        User.create_table()
        Admin.create_table()
        Zona.create_table()
        Event.create_table()
        Table.create_table()
        TableReservationHistory.create_table()

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
                for i in range(1, 19):
                    Table.create(number_table=i)
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
    name_event = CharField()
    description_event = CharField()
    creation_time = DateTimeField(default=datetime.datetime.now)
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
    number_table = IntegerField()
    number_of_seats = IntegerField(null=True)
    zona = ForeignKeyField(Zona, backref='zona', null=True)

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

    class Meta:
        db_table = 'party_reservation_history'


