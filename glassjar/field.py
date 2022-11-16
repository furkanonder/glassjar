from typing import Any, Callable


class Field:
    def __init__(self, name: str, field_type: Callable) -> None:
        self.name = name
        self.storage_name = f"_{name}"
        self.field_type = field_type

    def __get__(self, instance: Any, owner: Any = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if self.field_type != type(value):
            raise TypeError(
                f"Types are incompatible. Expected type: {self.field_type} | Given type: {type(value)}"
            )
        setattr(instance, self.storage_name, value)
