import psycopg2
from pprint import pprint

from db_class import db

if __name__ == '__main__':

    with psycopg2.connect(database="myclients_db", user="postgres", password="password1") as conn:
        clients = db(conn)
        print('Выберите действие:')
        print('1 - Создание струкруты БД')
        print('2 - Добавить нового клиента')
        print('3 - Добавить телефон для существующего клиента')
        print('4 - Изменить данные о клиенте')
        print('5 - Удалить телефон для существующего клиента.')
        print('6 - Удалить существующего клиента')
        print('7 - Найти клиента по его данным: имени, фамилии, email или телефону')
        action = int(input('Введите номер:'))
        if action == 1:
            clients.create_db(conn)
        elif action == 2:
            name = input('Введите имя клиента:')
            last_name = input('Введите фамилию клиента:')
            email = input('Введите email клиента:')
            numbers = int(input('Сколько будет номеров телефона у клиента?:'))
            if numbers == 0:
                phones = None
            else:
                phones = []
                for i in range(numbers):
                    phone = input('Введите номер:')
                    phones[numbers] = phone
            clients.add_client(conn, name, last_name, email, phones)
        elif action == 3:
            id = input('Введите id клиента:')
            phone = input('Введите номер:')
            clients.add_phone(conn, id, phone)
        elif action == 4:
            id = input('Введите id клиента:')
            name = input('Введите имя клиента:')
            last_name = input('Введите фамилию клиента:')
            email = input('Введите email клиента:')
            numbers = int(input('Сколько будет номеров телефона у клиента?:'))
            if numbers == 0:
                phones = None
            else:
                phones = []
                for i in range(numbers):
                    phone = input('Введите номер:')
                    phones[numbers] = phone
            clients.change_client(conn, id, name, last_name, email, phones)
        elif action == 5:
            id = input('Введите id клиента:')
            phone = input('Введите номер телефона клиента для удаления:')
            clients.delete_phone(conn, id, 'phone')
        elif action == 6:
            id = input('Введите id клиента:')
            clients.delete_client(conn, id)
        elif action == 7:
            name = input('Введите имя клиента:')
            last_name = input('Введите фамилию клиента:')
            email = input('Введите email клиента:')
            phone = input('Введите номер телефона клиента:')
            pprint(clients.find_client(conn, name, last_name, email, phone))
    conn.close()