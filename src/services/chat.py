from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
)
from sqlalchemy import (
    and_,
    desc,
    or_,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src import (
    ChatMessageModel,
    ChatRequestModel,
)
from src.deps.db import get_async_session
from src.enums.chat import RequestStatus
from src.schemas.chat.dto import (
    Chat,
    ChatCreateRequestSchema,
    ChatDetailResponse,
    ChatFilterParams,
    ChatMessageResponse,
    ChatUpdateStatusRequestSchema,
    ChatUser,
    MessageRequest,
)


class ChatService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
    ):
        self._session = session

    async def get_chat_list(
        self, limit: int, offset: int, user_id: UUID, filter_params: ChatFilterParams
    ) -> list[Chat]:
        chats = await self._session.scalars(
            select(ChatRequestModel)
            .options(joinedload(ChatRequestModel.requester), joinedload(ChatRequestModel.requested))
            .where(
                or_(ChatRequestModel.requester_id == user_id, ChatRequestModel.requested_id == user_id),
                ChatRequestModel.status == filter_params.status,
            )
            .limit(limit)
            .offset(offset)
        )

        return [
            Chat(
                user=(chat.requester if chat.requested_id == user_id else chat.requested),
                has_unread_messages=chat.has_unread_messages,
                status=chat.status,
                id=chat.id,
            )
            for chat in chats
        ]

    async def get_chat_details(self, chat_id: UUID, user_id: UUID) -> ChatDetailResponse:
        chat = await self._session.scalar(
            select(ChatRequestModel)
            .options(joinedload(ChatRequestModel.requester), joinedload(ChatRequestModel.requested))
            .where(
                ChatRequestModel.id == str(chat_id),
                or_(ChatRequestModel.requested_id == str(user_id), ChatRequestModel.requester_id == str(user_id)),
            )
        )
        if chat is None:
            raise HTTPException(status_code=404, detail="The chat room doesn't exist.")

        user = chat.requested if chat.requester_id == user_id else chat.requester

        return ChatDetailResponse(
            id=chat.id,
            has_unread_messages=chat.has_unread_messages,
            user_data=ChatUser.from_orm(user),
        )

    async def create_message(self, chat_id: UUID, sender_id: UUID, message_data: MessageRequest) -> None:
        chat = await self._session.scalar(
            select(ChatRequestModel).where(
                ChatRequestModel.id == chat_id,
                ChatRequestModel.status == RequestStatus.ACCEPTED.value,
                or_(ChatRequestModel.requester_id == sender_id, ChatRequestModel.requested_id == sender_id),
            )
        )
        if chat is None:
            raise HTTPException(status_code=404, detail="The chat does not exist.")

        chat_message = ChatMessageModel(chat_id=str(chat_id), sender_id=str(sender_id), message=message_data.message)
        chat.has_unread_messages = True
        self._session.add(chat)
        self._session.add(chat_message)

        try:
            await self._session.commit()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Something went wrong.")

    async def create_chat_request(self, user_id: UUID, schema: ChatCreateRequestSchema) -> None:
        if user_id == schema.user_id:
            raise HTTPException(status_code=400, detail="You cannot request a chat with yourself.")

        chat_request = await self._session.scalar(
            select(ChatRequestModel).where(
                or_(
                    and_(
                        ChatRequestModel.requester_id == str(user_id),
                        ChatRequestModel.requested_id == str(schema.user_id),
                    ),
                    and_(
                        ChatRequestModel.requested_id == str(user_id),
                        ChatRequestModel.requester_id == str(schema.user_id),
                    ),
                )
            )
        )
        if chat_request is not None:
            raise HTTPException(status_code=400, detail="The chat request already exists.")

        chat_request = ChatRequestModel(requester_id=str(user_id), requested_id=str(schema.user_id))
        self._session.add(chat_request)

        try:
            await self._session.commit()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Something went wrong.")

    async def update_chat_status(
        self,
        user_id: UUID,
        chat_id: UUID,
        schema: ChatUpdateStatusRequestSchema,
    ):
        chat_request = await self._session.scalar(
            select(ChatRequestModel).where(
                ChatRequestModel.id == str(chat_id), ChatRequestModel.requested_id == str(user_id)
            )
        )
        if chat_request is None:
            raise HTTPException(status_code=404, detail="The chat request does not exist.")

        chat_request.status = schema.status
        self._session.add(chat_request)

        try:
            await self._session.commit()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Something went wrong.")

    async def get_chat_messages(
        self, limit: int, offset: int, chat_id: UUID, user_id: UUID
    ) -> list[ChatMessageResponse]:
        chat = await self._session.scalar(
            select(ChatRequestModel).where(
                ChatRequestModel.id == chat_id,
                or_(ChatRequestModel.requester_id == user_id, ChatRequestModel.requested_id == user_id),
            )
        )
        if chat is None:
            raise HTTPException(status_code=404, detail="The chat does not exist.")

        messages = (
            await self._session.scalars(
                select(ChatMessageModel)
                .options(joinedload(ChatMessageModel.chat))
                .where(
                    ChatMessageModel.chat_id == chat_id,
                )
                .order_by(desc(ChatMessageModel.created_at))
                .limit(limit)
                .offset(offset)
            )
        ).all()

        if offset == 0 and len(messages) > 0 and messages[0].sender_id != user_id:
            messages[0].chat.has_unread_messages = False
            self._session.add(messages[0])
            try:
                await self._session.commit()
            except IntegrityError:
                raise HTTPException(status_code=400, detail="Something went wrong.")

        return [ChatMessageResponse.from_orm(message) for message in messages]
