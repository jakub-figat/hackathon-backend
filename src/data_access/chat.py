from uuid import UUID

from sqlalchemy import (
    or_,
    select,
)
from sqlalchemy.sql.expression import func

from src.data_access.base import BaseAsyncPostgresDataAccess
from src.models.chat import (
    ChatMessageModel,
    ChatRequestModel,
)
from src.schemas.chat.data_access import (
    ChatRequestInputSchema,
    ChatRequestSchema,
)


class ChatRequestDataAccess(BaseAsyncPostgresDataAccess[ChatRequestModel, ChatRequestInputSchema, ChatRequestSchema]):
    _model = ChatRequestModel
    _input_schema = ChatRequestInputSchema
    _output_schema = ChatRequestSchema

    async def get_latest_chats(self, user_id: UUID) -> list[ChatRequestSchema]:
        subquery = (
            select(ChatMessageModel.chat_id, func.max(ChatMessageModel.created_at))
            .group_by(ChatMessageModel.chat_id)
            .subquery()
        )

        statement = (
            select(self._model)
            .where(or_(self._model.requested_id == str(user_id), self._model.requester_id == str(user_id)))
            .join(subquery, self._model.id == subquery.c.chat_id)
        )

        print(statement)
        return await self._session.scalars(statement)
