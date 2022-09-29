from sqlalchemy.orm import (
    joinedload,
    selectinload,
)

from src import ChatMessageModel
from src.data_access.base import BaseAsyncPostgresDataAccess
from src.schemas.message.data_access import ChatMessageSchema
from src.services.chat import ChatMessageInputSchema


class ChatMessageDataAccess(BaseAsyncPostgresDataAccess[ChatMessageModel, ChatMessageInputSchema, ChatMessageSchema]):
    _model = ChatMessageModel
    _input_schema = ChatMessageInputSchema
    _output_schema = ChatMessageSchema

    @property
    def _base_select(self):
        return super()._base_select.options(joinedload("requester", "requested"), selectinload(self._model.messages))
