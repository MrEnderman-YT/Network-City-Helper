class DotenvDefaultData:
    def __init__(self,
                 bot_token: str,
                 host: str,
                 port: int,
                 user: str,
                 password: str,
                 database: str,
                 key: str,
                 ):
        self.bot_token = bot_token
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.key = key
