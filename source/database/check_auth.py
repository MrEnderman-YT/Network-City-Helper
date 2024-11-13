# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_auth_check:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def auth_check(self, member_id, full_mode):
        try:
            self.cursor.execute("SELECT login, password FROM members WHERE member_id = %s", (member_id,))
            existing_auth = self.cursor.fetchone()

            if full_mode == "str":

                if existing_auth["login"] is None and existing_auth["password"] is None:
                    return "doesnt exist"
                else:
                    login = existing_auth["login"]
                    password = existing_auth["password"]
                    return login, password

            elif full_mode:

                if existing_auth["login"] is None and existing_auth["password"] is None:
                    return "doesnt exist"
                else:
                    return "exist"

            elif not full_mode:

                if existing_auth["login"] is None or existing_auth["password"] is None:
                    return "doesnt exist"
                else:
                    return "exist"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
