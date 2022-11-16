import pickle
from typing import Any, ClassVar, Dict

from glassjar.constants import DB_NAME
from glassjar.db import DB, DatabaseManager, create_table
from glassjar.field import Field
from glassjar.query import QueryManager


class BaseModel(type):
    def __new__(mcs, cls_name: str, bases: tuple, cls_dict: Any) -> type:
        slots = []
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


class Model(DatabaseManager, metaclass=BaseModel):
    records: ClassVar[QueryManager]

    def __init__(self, **fields: Any) -> None:
        super().__init__(**fields)

    def __repr__(self) -> str:
        kwargs = ", ".join(
            f"{key}={getattr(self, key)!r}" for key in self.fields
        )
        return f"{type(self).__name__}({kwargs})"

    @property
    def as_dict(self) -> Dict[str, Any]:
        return {key: getattr(self, key) for key in self.fields}

    def update(self) -> None:
        self._update_record()

    def delete(self, id: int) -> None:
        self._delete_record(id)

    def save(self) -> "Model":
        if hasattr(self, "id"):
            self._update_record()
        else:
            self._create_record()
        return self

    def _create_record(self) -> "Model":
        with DB(DB_NAME, write_back=True) as db:
            table = db.db["tables"][self.table_name]
            setattr(self, "id", table["index"])
            table["records"].update({table["index"]: pickle.dumps(self)})
            table["index"] += 1
        return self
