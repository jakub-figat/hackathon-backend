from enum import Enum


class TokenType(str, Enum):
    refresh = "refresh"
    access = "access"
