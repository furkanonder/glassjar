from glassjar.db import DatabaseManager
from glassjar.query import QueryManager


class Field:
    def __init__(self, name):
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class BaseModel(type):
    def __new__(mcs, cls_name, bases, cls_dict):
        slots = []
        fields = cls_dict.get("__annotations__", {})

        for field_name, field_type in fields.items():
            field = Field(field_name)
            cls_dict[field_name] = field
            slots.append(field.storage_name)

        cls_dict["__slots__"] = slots

        obj = super().__new__(mcs, cls_name, bases, cls_dict)
        setattr(obj, "records", QueryManager(cls_name))

        return obj


class Model(DatabaseManager, metaclass=BaseModel):
    records = None

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
        self.update_record()

    def delete(self, id):
        self.delete_record(id)

    def save(self):
        if getattr(self, "id"):
            self.update_record()
        else:
            self.create_record()
        return self
