from src.data_access.base import BaseAsyncPostgresDataAccess
from src.models.user import UserModel
from src.schemas.user import UserRegisterSchema, UserSchema


class UserDataAccess(BaseAsyncPostgresDataAccess[UserModel, UserRegisterSchema, UserSchema]):
    _input_schema = UserRegisterSchema
    _output_schema = UserSchema
    _model = UserModel
