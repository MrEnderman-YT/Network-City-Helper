import os
import pymysql
from source.utils.dotenv_utils import get_dotenv_data


class DB_Connection:
    def __init__(self):
        env_data = get_dotenv_data()

        self.db = pymysql.connect(
            host=env_data.host,
            port=3306,
            user=env_data.user,
            password=env_data.password,
            database=env_data.database,
            cursorclass=pymysql.cursors.DictCursor
        )
