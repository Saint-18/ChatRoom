import os
import dotenv


def set_env_vars():
    config = dotenv.dotenv_values(".env")
    print(config.get("DATABASE_USER"))


def set_env_variables():
    """
    Sets defined environment variables
    Must be run any time values are changed the virtual environment

    """
    os.environ["db_user"] = "cs410"
    os.environ["db_passwd"] = "410group"


def verify():
    print(os.environ.get("db_user"))
    print(os.environ.get("db_passwd"))


if __name__ == "__main__":
    set_env_vars()
