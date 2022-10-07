from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    Type,
    TypeVar,
)
from uuid import UUID

from fastapi import Depends
from pydantic.main import BaseModel
from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.db import get_async_session
from src.exceptions.data_access import (
    ObjectAlreadyExists,
    ObjectNotFound,
)
from src.utils.schemas import BaseInputSchema


Model = TypeVar("Model")
InputSchema = TypeVar("InputSchema", bound=BaseInputSchema)
OutputSchema = TypeVar("OutputSchema", bound=BaseModel)


class BaseAsyncPostgresDataAccess(Generic[Model, InputSchema, OutputSchema], ABC):
    @property
    @abstractmethod
    def _input_schema(self) -> Type[InputSchema]:
        pass

    @property
    @abstractmethod
    def _output_schema(self) -> Type[OutputSchema]:
        pass

    @property
    @abstractmethod
    def _model(self) -> Type[Model]:
        pass

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self._session = session

    async def get_by(self, **kwargs):
        statement = self._base_select.where(*[getattr(self._model, key) == value for key, value in kwargs.items()])

        if (model := (await self._session.scalar(statement))) is None:
            params = ", ".join(f"{key}={value}" for key, value in kwargs.items())
            raise ObjectNotFound(f"The {self._model.__name__} with {params} does not exist.")

        return self._output_schema.from_orm(model)

    async def get_by_id(self, id: UUID) -> OutputSchema:
        statement = self._base_select.where(self._model.id == id)

        if (model := (await self._session.scalar(statement))) is None:
            raise ObjectNotFound(f"The object with id={id} does not exist.")

        return self._output_schema.from_orm(model)

    async def get_many(self, limit: int = 50, offset: int = 0) -> list[OutputSchema]:
        statement = self._base_select.limit(limit).offset(offset)
        return [self._output_schema.from_orm(model) for model in await self._session.scalars(statement)]

    async def create(self, input_schema: InputSchema) -> OutputSchema:
        model = self._model(**input_schema.to_orm_kwargs())
        self._session.add(model)

        try:
            await self._session.commit()
        except IntegrityError:
            raise ObjectAlreadyExists(f"Unique constraint violation for model {self._model.__name__}")

        return self._output_schema.from_orm(model)

    async def update(self, update_schema: InputSchema, id: UUID) -> OutputSchema:
        statement = self._base_select.where(self._model.id == id)

        if (model := (await self._session.scalar(statement))) is None:
            raise ObjectNotFound(f"The object with id={id} does not exist.")

        for key, value in update_schema.to_orm_kwargs().items():
            setattr(model, key, value)

        await self._session.commit()

        return self._output_schema.from_orm(model)

    async def delete_by_id(self, id: UUID) -> None:
        statement = delete(self._model).where(self._model.id == id)
        if (await self._session.scalar(select(self._model).where(self._model.id == id))) is None:
            raise ObjectNotFound(f"The object with id={id} does not exist.")

        await self._session.execute(statement)

    @property
    def _base_select(self):
        return select(self._model)
