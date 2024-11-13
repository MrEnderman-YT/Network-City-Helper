from dotenv import dotenv_values

from source.models.models import DotenvDefaultData


def get_dotenv_data() -> DotenvDefaultData:

    env_values = dotenv_values(".env")

    values = [value for key, value in env_values.items()]

    return DotenvDefaultData(*values)