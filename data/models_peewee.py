import datetime
import logging

from peewee import (CharField, DateTimeField, SqliteDatabase, DateField,
                    IntegerField, BooleanField, ForeignKeyField)
from peewee import Model, InternalError, PrimaryKeyField


def create_models() -> None:
    """
    Создание БД
    :return: None
    """
    try:

        User.create_table()
        Event.create_table()
        Table.create_table()
        TableReservationHistory()

        with db_beahea.atomic():
            for table in Table.select():
                table.delete_instance()
            for num in range(1, 20):
                x = num % 4
                if x == 0:
                    Zona.create(name='VIP')
                    Table.create(number_table=num, number_of_seats=4, zona=1)
                elif x == 1:
                    Zona.create(name='Bar')
                    Table.create(number_table=num, number_of_seats=6, zona=2)
                elif x == 2:
                    Zona.create(name='Central')
                    Table.create(number_table=num, number_of_seats=8, zona=3)
                elif x == 3:
                    Zona.create(name='Restoration')
                    Table.create(number_table=num, number_of_seats=2, zona=4)
    except InternalError as pw:
        logging.error(pw)


db_beahea = SqliteDatabase('C:/Users/dblmo/PycharmProjects/WhiteStarTeleBot/data/database.db')


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
    name = CharField(name=CharField(max_length=63, null=True))
    username = CharField(name=CharField(max_length=63, null=True))

    class Meta:
        db_table = "user"


class Event(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name_event = CharField()

    class Meta:
        db_table = "event"


class Zona(BaseUserModel):
    id = PrimaryKeyField(unique=True)
    name_zona = CharField()

    class Meta:
        db_table = "zona"


class Table(BaseUserModel):
    number_table = IntegerField()
    number_of_seats = IntegerField()
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
