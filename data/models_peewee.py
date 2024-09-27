import datetime
import logging

from peewee import (CharField, DateTimeField, SqliteDatabase, MySQLDatabase, DateField, PostgresqlDatabase,
                    IntegerField, BooleanField, ForeignKeyField)
from peewee import Model, InternalError, PrimaryKeyField

from config.config import DB_LOGIN, DB_PASSWORD


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
        data_tables = [
            {'number_table': 1},
        ]

        User.create_table()
        Event.create_table()
        Table.create_table()
        TableReservationHistory()

        with db_beahea.atomic():
            for zona in Zona.select():
                zona.delete_instance()
            for data_dict in data_zona:
                Zona.create(**data_dict)

            for table in Table.select():
                table.delete_instance()
            for i in range(1, 20):
                Table.create(number_table=i)
    except InternalError as pw:
        logging.error(pw)


db_beahea = MySQLDatabase('j10277899_whitestar',
                          register_hstore=True,
                          user=DB_LOGIN,
                          password=DB_PASSWORD,
                          host='mysql.32b20e713c92.hosting.myjino.ru/',
                          port='3306')


class BaseUserModel(Model):
    class Meta:
        database = db_beahea
        order_by = 'id'


class User(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    user_id = CharField(unique=True)
    creation_time = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True, null=True)

    phone = CharField(null=True)
    name = CharField(max_length=63, null=True)
    gender = CharField(null=True)
    date_birth = DateTimeField(null=True)
    username = CharField(max_length=63, null=True)

    class Meta:
        db_table = "user"


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
    user = ForeignKeyField(User, backref='user')
    table = ForeignKeyField(Table, backref='table')
    event = ForeignKeyField(Event, backref='event', null=True)
    creation_time = DateTimeField(default=datetime.datetime.now)
    booking_start_time = DateTimeField()
    booking_end_time = DateTimeField()
    number_of_guests = IntegerField()

    class Meta:
        db_table = 'table_reservation_history'
