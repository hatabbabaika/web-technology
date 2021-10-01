import sqlite3
import constants

DB_NAME = ''


class Connection:
    def __init__(self):
        self.connection = sqlite3.connect(constants.DB_NAME, check_same_thread=False)

    def __del__(self):
        self.commit()
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def exec_query(self, query, *params):
        cursor = self.connection.cursor()
        cursor.execute(query, {str(i): value for i, value in enumerate(params, 1)})
        response = cursor.fetchall()
        self.commit()
        cursor.close()
        return response
