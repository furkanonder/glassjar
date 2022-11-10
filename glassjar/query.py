import pickle
from typing import Any

from glassjar.constants import DB_NAME
from glassjar.db import DB
from glassjar.exceptions import DoesNotExist


class QueryManager:
    def __init__(self, name: str) -> None:
        self.table_name = f"{name}_table"

    def get(self, id: int) -> Any:
        with DB(DB_NAME, write_back=True) as db:
            try:
                obj = db.db["tables"][self.table_name]["records"][id]
                return pickle.loads(obj)
            except KeyError:
                raise DoesNotExist("Object does not exist.")

    def all(self) -> list:
        with DB(DB_NAME, write_back=True) as db:
            try:
                values = db.db["tables"][self.table_name]["records"].values()
                objs = [pickle.loads(val) for val in values]
                return objs
            except KeyError:
                return []

    def count(self) -> int:
        return len(self.all())

    def first(self) -> Any:
        try:
            return self.all()[0]
        except IndexError:
            return []

    def last(self) -> Any:
        try:
            return self.all()[-1]
        except IndexError:
            return []
