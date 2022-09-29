from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.deps.jwt import get_verified_user
from src.schemas.chat.dto import (
    Chat,
    ChatCreateRequestSchema,
    ChatDetailResponse,
    ChatFilterParams,
    ChatMessageResponse,
    ChatUpdateStatusRequestSchema,
    MessageRequest,
)
from src.schemas.paging import (
    PaginatedResponseSchema,
    PagingInputParams,
)
from src.schemas.user.data_access import UserSchema
from src.services.chat import ChatService


chat_router = APIRouter(tags=["chat"])


@chat_router.get("/", response_model=PaginatedResponseSchema[Chat])
async def chats_list(
    user: UserSchema = Depends(get_verified_user),
    chat_service: ChatService = Depends(),
    paging_params: PagingInputParams = Depends(),
    filter_params: ChatFilterParams = Depends(),
) -> PaginatedResponseSchema[Chat]:
    chats = await chat_service.get_chat_list(
        *paging_params.to_limit_offset(), user_id=user.id, filter_params=filter_params
    )

    return PaginatedResponseSchema[Chat].from_results(results=chats, page_number=paging_params.page_number)


@chat_router.post("/{chat_id}/messages/", status_code=status.HTTP_204_NO_CONTENT)
async def create_message(
    chat_id: UUID,
    message_request: MessageRequest,
    user: UserSchema = Depends(get_verified_user),
    chat_service: ChatService = Depends(),
) -> None:
    await chat_service.create_message(chat_id=chat_id, sender_id=user.id, message_data=message_request)


@chat_router.patch("/{chat_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_chat_status(
    chat_id: UUID,
    schema: ChatUpdateStatusRequestSchema,
    user: UserSchema = Depends(get_verified_user),
    chat_service: ChatService = Depends(),
):
    return await chat_service.update_chat_status(chat_id=chat_id, user_id=user.id, schema=schema)


@chat_router.get("/{chat_id}/", response_model=ChatDetailResponse)
async def chats_detail(
    chat_id: UUID, user: UserSchema = Depends(get_verified_user), chat_service: ChatService = Depends()
) -> ChatDetailResponse:
    return await chat_service.get_chat_details(chat_id=chat_id, user_id=user.id)


@chat_router.get("/{chat_id}/messages/", response_model=PaginatedResponseSchema[ChatMessageResponse])
async def get_chat_messages(
    chat_id: UUID,
    user: UserSchema = Depends(get_verified_user),
    chat_service: ChatService = Depends(),
    paging_params: PagingInputParams = Depends(),
):
    messages = await chat_service.get_chat_messages(*paging_params.to_limit_offset(), chat_id=chat_id, user_id=user.id)

    return PaginatedResponseSchema[ChatMessageResponse].from_results(
        results=messages, page_number=paging_params.page_number
    )


@chat_router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_chat(
    schema: ChatCreateRequestSchema,
    user: UserSchema = Depends(get_verified_user),
    chat_service: ChatService = Depends(),
):
    return await chat_service.create_chat_request(user_id=user.id, schema=schema)

