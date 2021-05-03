import sqlite3


class SQL_db:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file,
                                          check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM `subscriptions` WHERE `status` = ?",
                (status,)).fetchall()

    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                'SELECT * FROM `subscriptions` WHERE `user_id` = ?',
                (user_id,))
            res = result.fetchall()
            return bool(len(res))

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `subscriptions` (`user_id`, `status`) VALUES (?,?)",
                (user_id, status))

    def update_subscription(self, user_id, status):
        with self.connection:
            self.cursor.execute(
                "UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?",
                (status, user_id))

    def check_status(self, user_id):
        return str(self.cursor.execute(
            'SELECT `status` FROM `subscriptions` WHERE `user_id` = ?',
            (user_id,)).fetchone())

    def close(self):
        self.connection.close()
