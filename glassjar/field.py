from typing import Any


class Field:
    def __init__(self, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: Any, value: Any) -> None:
        setattr(instance, self.storage_name, value)
