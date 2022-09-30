from src.data_access.base import BaseAsyncPostgresDataAccess
from src.models.user import UserModel
from src.schemas.user import UserInputSchema, UserRegisterSchema, UserSchema
from src.utils.password import password_context


class UserDataAccess(BaseAsyncPostgresDataAccess[UserModel, UserInputSchema, UserSchema]):
    _input_schema = UserInputSchema
    _output_schema = UserSchema
    _model = UserModel

    async def register_user(self, input_schema: UserRegisterSchema) -> UserSchema:
        input_schema.password = password_context.hash(input_schema.password)
        return await super().create(input_schema=input_schema)
