import shelve

from glassjar.constants import DB_NAME
from glassjar.exceptions import DoesNotExist


class QueryManager:
    def __init__(self, name):
        self.table_name = f"{name}_table"

    def get(self, id):
        with shelve.open(DB_NAME, writeback=True) as db:
            try:
                obj = db["tables"][self.table_name]["records"][id]
                return obj
            except KeyError:
                raise DoesNotExist("Object does not exist.")

    def all(self):
        with shelve.open(DB_NAME, writeback=True) as db:
            try:
                return list(db["tables"][self.table_name]["records"].values())
            except KeyError:
                return []

    def count(self):
        return len(self.all())

    def first(self):
        try:
            return self.all()[0]
        except IndexError:
            return []

    def last(self):
        try:
            return self.all()[-1]
        except IndexError:
            return []
