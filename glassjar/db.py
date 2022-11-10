import contextlib
import os
import pickle
from io import BytesIO
from pickle import Pickler, Unpickler

from glassjar.constants import DB_NAME
from glassjar.exceptions import DoesNotExist


class DB:
    def __init__(self, file_name, write_back=False):
        self.file_name = file_name
        self.write_back = write_back
        self.cache = {}
        self.db = {}
        self.create_or_set_db()

    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            value = Unpickler(BytesIO(self.db[key])).load()
            if self.write_back:
                self.cache[key] = value
        return value

    def __setitem__(self, key, value):
        if self.write_back:
            self.cache[key] = value
        f = BytesIO()
        Pickler(f, pickle.HIGHEST_PROTOCOL).dump(value)
        self.db[key] = f.getvalue()

    def __delitem__(self, key):
        del self.db[key]
        with contextlib.suppress(KeyError):
            del self.cache[key]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def create_or_set_db(self):
        try:
            if os.path.getsize(self.file_name):
                with open(self.file_name, "rb") as fp:
                    self.db = pickle.load(fp)
        except FileNotFoundError:
            self.db["tables"] = {}
            with open(self.file_name, "wb") as fp:
                fp.write(b"")

    def get(self, key, default=None):
        if key in self.db:
            return self.db[key]
        return default

    def close(self):
        if self.write_back and self.cache:
            for key, entry in self.cache.items():
                self[key] = entry
            self.cache = {}
        with open(self.file_name, "wb") as fp:
            pickle.dump(self.db, fp)

    def initialize_table(self, table_name):
        if self.db["tables"].get(table_name) is None:
            self.db["tables"][table_name] = {"index": 1, "records": {}}


class DatabaseManager:
    __slots__ = "fields"
    table_name: str
    id: int

    def __init__(self, **fields):
        self.fields = fields
        for field_name, field_value in self.fields.items():
            setattr(self, field_name, field_value)

    def _get_record(self, id):
        with DB(DB_NAME, write_back=True) as db:
            try:
                obj = db.db["tables"][self.table_name]["records"][id]
                return obj
            except KeyError:
                raise DoesNotExist("Object does not exist.")

    def _set_record(self, id, value):
        with DB(DB_NAME, write_back=True) as db:
            value = pickle.dumps(value)
            db.db["tables"][self.table_name]["records"][id] = value

    def _update_record(self):
        db_obj = pickle.loads(self._get_record(self.id))

        for field_name, field_value in self.fields.items():
            obj_value = getattr(self, field_name)
            if getattr(db_obj, field_name) != obj_value:
                setattr(db_obj, field_name, obj_value)

        self._set_record(self.id, db_obj)

    def _create_record(self):
        with DB(DB_NAME, write_back=True) as db:
            table = db.db["tables"][self.table_name]
            setattr(self, "id", table["index"])
            table["records"].update({table["index"]: pickle.dumps(self)})
            table["index"] += 1
        return self

    def _delete_record(self, id):
        with DB(DB_NAME, write_back=True) as db:
            try:
                del db.db["tables"][self.table_name]["records"][id]
            except KeyError:
                raise DoesNotExist("Object does not exist.")


def create_table(table_name):
    with DB(DB_NAME, write_back=True) as db:
        db.initialize_table(table_name)
