from enum import Enum


class UserRole(str, Enum):
    STANDARD = "STANDARD"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"
