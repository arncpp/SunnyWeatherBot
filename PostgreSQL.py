import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error


class postgres_db:
    """
    База данных heroku PostgreSQL
    """

    def __init__(self):
        self.connection = psycopg2.connect(user="------------",
                                           password="--------",
                                           host="------------",
                                           port="------------",
                                           database="--------")
        self.cursor = self.connection.cursor()
        self.table = '''CREATE TABLE subscriptions
                          (ID             INT       PRIMARY KEY   NOT NULL,
                          USER_ID         INT(255)                NOT NULL,
                          STATUS          BOOL); '''

    def create_db(self):
        """
        Создание базы данных, но глобальная база данных создается
        через консоль или на сайте Heroku
        """
        try:
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor.execute('create database -------------')
        except (Exception, Error):
            print("База данных уже была создана")

    def create_table(self):
        """
        Создание таблицы в базе данных, но в глобальной базе данных на Хероку
        она создается через консоль с помощью команды heroku pg:psql
        :return:
        """
        try:
            self.cursor.execute(self.table)
            self.connection.commit()
            print(self.table)
        except (Exception, Error):
            print("Таблица уже была создана")

    def get_subscriptions(self, status=True):
        """
        Получить всех подписчиков, которыеподписаны на рассылку
        :param status: True
        :return: список кортежей
        """
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM subscriptions WHERE STATUS = {status}")
            return self.cursor.fetchall()

    def subscriber_exists(self, user_id):
        """
        Проверяет, есть ли пользователь в базе данных
        :param user_id: id пользователя
        :return: True or False
        """
        with self.connection:
            self.cursor.execute(
                f'SELECT * FROM subscriptions WHERE USER_ID = {user_id}')
            res = self.cursor.fetchall()
            print(bool(len(res)))
            return bool(len(res))

    def add_subscriber(self, user_id, status=True):
        """
        Добавляет пользователя в базу данных, дает ему подписку
        :param user_id: id пользователя
        :param status: статус подписки
        :return:
        """
        with self.connection:
            print("Подписка")
            self.cursor.execute("SELECT ID FROM subscriptions")
            rows = self.cursor.fetchall()
            id_tab = 1
            for row in rows:
                id_tab += 1
            return self.cursor.execute(
                f"INSERT INTO subscriptions (ID, USER_ID, STATUS) VALUES {(id_tab, user_id, status)}")

    def update_subscription(self, user_id, status):
        """
        Если пользователь есть в баззе данных, то обновляет ему статус подписки
        (если он отписался или подписался снова)
        :param user_id: id пользователя
        :param status: статус подписки
        :return:
        """
        with self.connection:
            self.cursor.execute(
                f"UPDATE subscriptions SET STATUS = {status} WHERE USER_ID = {user_id}")

    def check_status(self, user_id):
        """
        Проверка статуса подписки
        :param user_id: id пользователя
        :return: True or False
        """
        self.cursor.execute(
            f'SELECT STATUS FROM subscriptions WHERE USER_ID = {user_id}')
        status = self.cursor.fetchone()
        print(status)

        return str(status)

    def print_info(self):
        """
        Печатает всю базу данных
        """
        self.cursor.execute("SELECT * FROM subscriptions")
        rows = self.cursor.fetchall()
        for row in rows:
            print("ID", row[0])
            print("USER_ID", row[1])
            print("STATUS", row[2])

    def close(self):
        """
        Закрывает соединение с базой данных
        """
        self.connection.close()
