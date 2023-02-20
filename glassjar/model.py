from __future__ import annotations

from typing import Any, ClassVar, Generic, NoReturn, Type, TypeVar

from glassjar.db import DB, create_table
from glassjar.field import Field

T = TypeVar("T", bound="Model")


class QuerySet(Generic[T]):
    def __init__(self, objs: list[T]) -> None:
        self.__objs = objs
        self.__index = 0

    def __iter__(self) -> "QuerySet":
        return self

    def __next__(self) -> T | NoReturn:
        try:
            obj = self.__objs[self.__index]
        except IndexError:
            raise StopIteration

        self.__index += 1
        return obj

    def __repr__(self) -> str:
        return f"<QuerySet {tuple(obj for obj in self.__objs)} >"

    def __len__(self) -> int:
        return len(self.__objs)

    def as_dict(self) -> dict[int, dict[str, Any]]:
        return {obj.id: obj.as_dict() for obj in self.__objs}

    def count(self) -> int:
        return len(self.__objs)

    def first(self) -> "QuerySet" | T:
        try:
            return self.__objs[0]
        except IndexError:
            return QuerySet([])

    def last(self) -> "QuerySet" | T:
        try:
            return self.__objs[-1]
        except IndexError:
            return QuerySet([])


class QueryManager(Generic[T]):
    def __init__(self, name: str) -> None:
        self.table_name = f"{name}_table"

    def get(self, id: int) -> T:
        with DB(self.table_name) as db:
            obj = db.get_obj(id)
            return obj

    def all(self) -> QuerySet:
        with DB(self.table_name) as db:
            try:
                objs = db.get_objs()
                return QuerySet(objs)
            except KeyError:
                return QuerySet([])

    def count(self) -> int:
        return self.all().count()

    def first(self) -> QuerySet | T:
        return self.all().first()

    def last(self) -> QuerySet | T:
        return self.all().last()


class BaseModel(type):
    def __new__(
        mcs, cls_name: str, bases: tuple, cls_dict: Any
    ) -> Type[T] | "BaseModel":
        slots = ["fields"]
        fields = cls_dict.get("__annotations__", {})
        fields.update({"id": int})

        for field_name, field_type in fields.items():
            field = Field(field_name, field_type)
            cls_dict[field_name] = field
            slots.append(field.storage_name)

        cls_dict["__slots__"] = slots
        obj = super().__new__(mcs, cls_name, bases, cls_dict)
        setattr(obj, "records", QueryManager(cls_name))
        setattr(obj, "table_name", f"{cls_name}_table")
        create_table(f"{cls_name}_table")

        return obj


class Model(metaclass=BaseModel):
    table_name: ClassVar[str]
    id: ClassVar[int]
    records: ClassVar[QueryManager]

    def __init__(self, **fields: dict[str, Any]) -> None:
        self.fields = fields
        for field_name, field_value in self.fields.items():
            setattr(self, field_name, field_value)

    def __eq__(self, other):
        if self.as_dict == self.as_dict:
            return True
        else:
            return False

    def __repr__(self) -> str:
        kwargs = ", ".join(
            f"{key}={getattr(self, key)!r}" for key in self.fields
        )
        return f"{type(self).__name__}({kwargs})"

    def as_dict(self) -> dict[str, Any]:
        return {key: getattr(self, key) for key in self.fields}

    def update(self) -> None:
        with DB(self.table_name) as db:
            db.update_record(self.id, self)

    def delete(self, id: int) -> None:
        with DB(self.table_name) as db:
            db.delete_record(id)

    def save(self) -> "Model":
        if hasattr(self, "id"):
            self.update()
        else:
            with DB(self.table_name) as db:
                db.create_record(self)
        return self
