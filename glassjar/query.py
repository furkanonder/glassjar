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

    def first(self):
        return self.get(id=1)
