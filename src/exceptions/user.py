class UserServiceException(Exception):
    pass


class InvalidCredentials(UserServiceException):
    pass
