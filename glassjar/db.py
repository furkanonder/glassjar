import contextlib
import os
import pickle
from io import BytesIO
from pickle import Pickler, Unpickler
from types import TracebackType
from typing import Any, ClassVar, Hashable

from glassjar.constants import DB_NAME
from glassjar.exceptions import DoesNotExist


class DB:
    def __init__(self, file_name: str, write_back: bool = False):
        self.file_name = file_name
        self.write_back = write_back
        self.cache: dict = {}
        self.db: dict = {}
        self.create_or_set_db()

    def __getitem__(self, key: Hashable) -> Any:
        try:
            value = self.cache[key]
        except KeyError:
            value = Unpickler(BytesIO(self.db[key])).load()
            if self.write_back:
                self.cache[key] = value
        return value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.write_back:
            self.cache[key] = value
        f = BytesIO()
        Pickler(f, pickle.HIGHEST_PROTOCOL).dump(value)
        self.db[key] = f.getvalue()

    def __delitem__(self, key: Hashable) -> None:
        del self.db[key]
        with contextlib.suppress(KeyError):
            del self.cache[key]

    def __enter__(self) -> "DB":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        self.close()

    def create_or_set_db(self) -> None:
        try:
            if os.path.getsize(self.file_name):
                with open(self.file_name, "rb") as fp:
                    self.db = pickle.load(fp)
        except FileNotFoundError:
            self.db["tables"] = {}
            with open(self.file_name, "wb") as fp:
                fp.write(b"")

    def get(self, key: Hashable, default: Any = None) -> Any:
        if key in self.db:
            return self.db[key]
        return default

    def close(self) -> None:
        if self.write_back and self.cache:
            for key, entry in self.cache.items():
                self[key] = entry
            self.cache = {}
        with open(self.file_name, "wb") as fp:
            pickle.dump(self.db, fp)

    def initialize_table(self, table_name: str) -> None:
        if self.db["tables"].get(table_name) is None:
            self.db["tables"][table_name] = {"index": 1, "records": {}}


class DatabaseManager:
    __slots__ = "fields"
    table_name: ClassVar[str]
    id: ClassVar[int]

    def __init__(self, **fields: Any) -> None:
        self.fields = fields
        for field_name, field_value in self.fields.items():
            setattr(self, field_name, field_value)

    def _get_record(self, id: int) -> Any:
        with DB(DB_NAME, write_back=True) as db:
            try:
                obj = db.db["tables"][self.table_name]["records"][id]
                return obj
            except KeyError:
                raise DoesNotExist("Object does not exist.")

    def _set_record(self, id: int, value: Any) -> None:
        with DB(DB_NAME, write_back=True) as db:
            value = pickle.dumps(value)
            db.db["tables"][self.table_name]["records"][id] = value

    def _update_record(self) -> None:
        db_obj = pickle.loads(self._get_record(self.id))

        for field_name, field_value in self.fields.items():
            obj_value = getattr(self, field_name)
            if getattr(db_obj, field_name) != obj_value:
                setattr(db_obj, field_name, obj_value)

        self._set_record(self.id, db_obj)

    def _delete_record(self, id: int) -> None:
        with DB(DB_NAME, write_back=True) as db:
            try:
                del db.db["tables"][self.table_name]["records"][id]
            except KeyError:
                raise DoesNotExist("Object does not exist.")


def create_table(table_name: str) -> None:
    with DB(DB_NAME, write_back=True) as db:
        db.initialize_table(table_name)
