from __future__ import annotations

import os
import pickle
from types import TracebackType
from typing import TYPE_CHECKING, Any, Hashable, List

from glassjar.constants import DB_NAME
from glassjar.exceptions import DoesNotExist

if TYPE_CHECKING:
    from glassjar.model import Model


class DB:
    def __init__(self, table_name: str) -> None:
        self.db: dict[Hashable, Any] = {}
        self.table_name = table_name
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

    def initialize_table(self, table_name: str) -> None:
        if self.db["tables"].get(table_name) is None:
            self.db["tables"][table_name] = {"index": 1, "records": {}}

    def get_obj(self, _id: int) -> Model:
        try:
            record = self.db["tables"][self.table_name]["records"][_id]
            obj = pickle.loads(record)
            return obj
        except KeyError:
            raise DoesNotExist("Object does not exist.")

    def get_objs(self) -> List[Model]:
        records = self.db["tables"][self.table_name]["records"].values()
        objs = [pickle.loads(val) for val in records]
        return objs

    def delete_record(self, _id: int) -> None:
        try:
            del self.db["tables"][self.table_name]["records"][_id]
        except KeyError:
            raise DoesNotExist("Object does not exist.")

    def create_record(self, obj: Model) -> None:
        table = self.db["tables"][self.table_name]
        setattr(obj, "id", table["index"])
        table["records"].update({table["index"]: pickle.dumps(obj)})
        table["index"] += 1

    def update_record(self, _id: int, obj: Model) -> None:
        db_obj = self.get_obj(_id)

        for field_name, field_value in db_obj.fields.items():
            obj_value = getattr(obj, field_name)
            if getattr(db_obj, field_name) != obj_value:
                setattr(db_obj, field_name, obj_value)

        value = pickle.dumps(db_obj)
        self.db["tables"][self.table_name]["records"][_id] = value


def create_table(table_name: str) -> None:
    with DB(table_name) as db:
        db.initialize_table(table_name)
