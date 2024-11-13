# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_privacy_get:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def privacy_get(self, member_id):
        try:
            self.cursor.execute("SELECT privacy_policy FROM members WHERE member_id = %s", (member_id,))
            existing_privacy = self.cursor.fetchone()

            if not existing_privacy:
                return "doesnt exist"

            else:
                if existing_privacy["privacy_policy"] == 0:
                    existing_privacy = "0"
                elif existing_privacy["privacy_policy"] == 1:
                    existing_privacy = "1"
                return existing_privacy

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
