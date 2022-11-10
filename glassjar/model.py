from glassjar.db import DatabaseManager, create_table
from glassjar.query import QueryManager


class Field:
    def __init__(self, name, field_type):
        self.name = name
        self.storage_name = f"_{name}"
        self.field_type = field_type

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if self.field_type != type(value):
            raise TypeError(
                f"Types are incompatible. Expected type: {self.field_type} | Given type: {type(value)}"
            )
        setattr(instance, self.storage_name, value)


class BaseModel(type):
    def __new__(mcs, cls_name, bases, cls_dict):
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
    records: QueryManager

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self):
        kwargs = ", ".join(
            f"{key}={getattr(self, key)!r}" for key in self.fields
        )
        return f"{type(self).__name__}({kwargs})"

    @property
    def as_dict(self):
        return {key: getattr(self, key) for key in self.fields}

    def update(self):
        self._update_record()

    def delete(self, id):
        self._delete_record(id)

    def save(self):
        if hasattr(self, "id"):
            self._update_record()
        else:
            self._create_record()
        return self
