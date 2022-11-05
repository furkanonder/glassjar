import shelve

from glassjar.constants import DB_NAME
from glassjar.exceptions import DoesNotExist


class DatabaseManager:
    def __init__(self, **fields):
        self.cls = type(self)
        self.table_name = f"{self.cls.__name__}_table"
        self.create_table()
        self.fields = fields

        for field_name, field_value in fields.items():
            setattr(self, field_name, field_value)

    def create_table(self):
        with shelve.open(DB_NAME, writeback=True) as db:
            if db.get("tables") is None:
                db["tables"] = {}
            if db["tables"].get(self.table_name) is None:
                db["tables"][self.table_name] = {"index": 1, "records": {}}

    def get_record(self, id):
        with shelve.open(DB_NAME, writeback=True) as db:
            try:
                obj = db["tables"][self.table_name]["records"][id]
                return obj
            except KeyError:
                raise DoesNotExist("Object does not exist.")

    def set_record(self, id, value):
        with shelve.open(DB_NAME, writeback=True) as db:
            db["tables"][self.table_name]["records"][id] = value

    def update_record(self):
        db_obj = self.get_record(self.id)

        for field_name, field_value in self.fields.items():
            obj_value = getattr(self, field_name)
            if getattr(db_obj, field_name) != obj_value:
                setattr(db_obj, field_name, obj_value)

        self.set_record(self.id, db_obj)

    def create_record(self):
        with shelve.open(DB_NAME, writeback=True) as db:
            table = db["tables"][self.table_name]
            setattr(self, "id", table["index"])
            table["records"].update({table["index"]: self})
            table["index"] += 1
        return self

    def delete_record(self, id):
        with shelve.open(DB_NAME, writeback=True) as db:
            try:
                del db["tables"][self.table_name]["records"][id]
            except KeyError:
                raise DoesNotExist("Object does not exist.")
