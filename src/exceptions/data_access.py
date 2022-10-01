class DataAccessException(Exception):
    """Exception raised when a generic error occurs"""


class ObjectNotFound(DataAccessException):
    """Exception raised when an object was not found"""


class ObjectAlreadyExists(DataAccessException):
    """Exception raised when an object already exists"""
