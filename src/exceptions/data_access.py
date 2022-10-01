from typing import Any


class DataAccessException(Exception):
    pass


class ModelNotFound(DataAccessException):
    @classmethod
    def from_field(cls, field_name: str, value: Any, model_name: str) -> "ModelNotFound":
        return cls(f"{model_name} with {field_name}={value} not found")


class ModelAlreadyExists(DataAccessException):
    pass
