from glassjar.db import DatabaseManager
from glassjar.query import QueryManager


class Field:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class BaseModel(type):
    def __new__(mcs, cls_name, bases, cls_dict):
        obj = super().__new__(mcs, cls_name, bases, cls_dict)
        setattr(obj, "records", QueryManager(cls_name))
        return obj


class Model(DatabaseManager, metaclass=BaseModel):
    records = None

    def __init__(self, **fields):
        super().__init__(**fields)
        self.id = None

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
