import sqlite3


class Sql_lite:

    def __init__(self):
        self.conn = sqlite3.connect('db/database.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def write_to_the_database(self, id_user: int, first_name: str, last_name: str, username: str, date: str, person_name: str):
        """Запись пользователя в БД"""
        try:
            self.cursor.execute(
                'INSERT INTO data (id_user, first_name, last_name, username, date, person_name) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    id_user,
                    first_name,
                    last_name,
                    username,
                    date,
                    person_name,
                )
            )
            self.conn.commit()
        except sqlite3.Error as error:
            print("Ошибка при записи данных в БД SQLite", error)

    def search_name_in_database(self, person_name: str) -> bool:
        """Поиск имени человека, которому должны подарить подарок, в БД"""
        try:
            sql_select_query = """SELECT * FROM data WHERE person_name = ?"""
            self.cursor.execute(sql_select_query, (person_name,))
            records = self.cursor.fetchall()
            if len(records) > 0:
                return True
            else:
                return False
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def search_id_user_in_database(self, id_user: int):
        """Определение уникальности пользователя"""
        try:
            sql_select_query = """SELECT * FROM data WHERE id_user = ?"""
            self.cursor.execute(sql_select_query, (id_user,))
            record = self.cursor.fetchall()
            if len(record) > 0:
                return record[-1][-1]
            else:
                return False
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


    # def deleting_extra_entries(self):
    #     """Удаление лишних записей, начинается после 1000 шт"""
    #     if self.flag_db == 'True':
    #         try:
    #             while True:
    #                 sql_select_query = """SELECT * FROM data"""
    #                 self.cursor.execute(sql_select_query)
    #                 records = self.cursor.fetchall()
    #                 if len(records) > 1000:
    #                     sql_select_query = """DELETE FROM data WHERE id = (SELECT min(id) FROM data)"""
    #                     self.cursor.execute(sql_select_query)
    #                     self.conn.commit()
    #                 else:
    #                     break
    #         except sqlite3.Error as error:
    #             print("Ошибка при работе с SQLite", error)

