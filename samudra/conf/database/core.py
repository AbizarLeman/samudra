from contextvars import ContextVar
import logging
import os
from dataclasses import dataclass

import peewee as pw
from dotenv import load_dotenv

from samudra.conf.database.options import DatabaseEngine

load_dotenv()

# TODO Refactor these to depend on conf.toml
ENGINE = os.getenv('ENGINE')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT = int(os.getenv('DATABASE_PORT'))
DATABASE_OPTIONS = os.getenv('DATABASE_OPTIONS')
USERNAME = os.getenv('DATABASE_USERNAME')
PASSWORD = os.getenv('DATABASE_PASSWORD')
SSL_MODE = os.getenv('SSL_MODE')

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


def get_database(engine: DatabaseEngine) -> pw.Database:
    """
    Returns the connection class based on the engine.
    """
    if engine == DatabaseEngine.SQLite:
        # Defaults to make it async-compatible (according to FastAPI/Pydantic)
        class PeeweeConnectionState(pw._ConnectionState):
            def __init__(self, **kwargs):
                super().__setattr__("_state", db_state)
                super().__init__(**kwargs)

            def __setattr__(self, name, value):
                self._state.get()[name] = value

            def __getattr__(self, name):
                return self._state.get()[name]

        # The DB connection object
        return_db = pw.SqliteDatabase(os.path.join(os.getcwd(), 'data', f"{DATABASE_NAME}.db"))
        return_db._state = PeeweeConnectionState()

        logging.info(f'Connecting to {return_db.database}')
    elif engine == DatabaseEngine.MySQL:
        conn_str = f'mysql://{USERNAME}:{PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?ssl-mode=REQUIRED'
        return_db = pw.MySQLDatabase(conn_str)
        logging.info(f'Connecting to {return_db.database} as {USERNAME}')
    elif engine == DatabaseEngine.CockroachDB:
        from playhouse.cockroachdb import CockroachDatabase
        conn_str = f'postgresql://{USERNAME}:{PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?sslmode=verify-full&options={DATABASE_OPTIONS}'
        return_db = CockroachDatabase(conn_str)
        logging.info(f'Connecting to {return_db.database} as {USERNAME}')
    else:
        raise NotImplementedError("Invalid engine")
    return return_db


@dataclass
class Database:
    engine = DatabaseEngine[ENGINE]
    connection = get_database(engine=DatabaseEngine[ENGINE])