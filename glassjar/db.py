from __future__ import annotations

import os
import pickle
from types import TracebackType
from typing import Any, ClassVar, Hashable

from glassjar.constants import DB_NAME
from glassjar.exceptions import DoesNotExist


class DB:
    def __init__(self) -> None:
        self.db: dict[Hashable, Any] = {}
        self.create_or_get_db()

    def __enter__(self) -> "DB":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        with open(DB_NAME, "wb") as fp:
            pickle.dump(self.db, fp)

    def create_or_get_db(self) -> None:
        try:
            if os.path.getsize(DB_NAME):
                with open(DB_NAME, "rb") as fp:
                    self.db = pickle.load(fp)
        except FileNotFoundError:
            self.db["tables"] = {}
            with open(DB_NAME, "wb") as fp:
                fp.write(b"")

    def get(self, key: Hashable, default: Any = None) -> Any:
        if key in self.db:
            return self.db[key]
        return default

    def initialize_table(self, table_name: str) -> None:
        if self.db["tables"].get(table_name) is None:
            self.db["tables"][table_name] = {"index": 1, "records": {}}


class DatabaseManager:
    __slots__ = "fields"
    table_name: ClassVar[str]
    id: ClassVar[int]

    def __init__(self, **fields: dict[str, Any]) -> None:
        self.fields = fields
        for field_name, field_value in self.fields.items():
            setattr(self, field_name, field_value)

    def _get_record(self, id: int) -> bytes:
        with DB() as db:
            try:
                obj = db.db["tables"][self.table_name]["records"][id]
                return obj
            except KeyError:
                raise DoesNotExist("Object does not exist.")

    def _set_record(self, id: int, value: Any) -> None:
        with DB() as db:
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
        with DB() as db:
            try:
                del db.db["tables"][self.table_name]["records"][id]
            except KeyError:
                raise DoesNotExist("Object does not exist.")


def create_table(table_name: str) -> None:
    with DB() as db:
        db.initialize_table(table_name)
