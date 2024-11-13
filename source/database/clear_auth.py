# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_auth_clear:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def auth_clear(self, member_id):
        try:

            self.cursor.execute(
                "UPDATE members SET role = NULL, login = NULL, password = NULL, name = NULL, surname = NULL, class = NULL, notification_overdue_assignments = False, notification_timetable = False, notification_announcement = False WHERE member_id = %s",
                (member_id,)
            )
            self.db_conn.db.commit()
            return "ok"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
