import inspect
from typing import Any


class Field:
    def __init__(self, name: str, field_type: Any, validate: bool) -> None:
        self.name = name
        self.storage_name = f"_{name}"
        self.field_type = field_type
        self.validate = validate

    def __get__(self, instance: Any, owner: Any = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if self.validate:
            if inspect.isclass(value):
                if not (self.field_type is value):
                    raise TypeError(
                        f"Types are incompatible. Expected type: {self.field_type} | Given type: {value}"
                    )
            elif self.field_type != type(value):
                raise TypeError(
                    f"Types are incompatible. Expected type: {self.field_type} | Given type: {type(value)}"
                )
        setattr(instance, self.storage_name, value)
