from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AuthenticationCasesEnum(Enum):
    WRONG_AUTH_TOKEN = "wrong_token"
    WRONG_REFRESH_TOKEN = "wrong_refresh_token"
    SHOULD_BE_REFRESHED_AUTH_TOKEN = "should_be_refreshed"
    TOKEN_HAS_BEEN_REFRESHED = "token_has_been_refreshed"
    TOKEN_IS_ALIVE = "token_is_alive"
    TOKEN_HAS_BEEN_REVOKED = "token_has_been_revoked"


@dataclass
class UserRegistrationInfo:
    login: str
    email: str


@dataclass
class UserAuthenticationInfo:
    login: str
    password: str


@dataclass
class UserInfoInToken:
    login: str
    email: str


@dataclass
class AuthToken:
    data: UserInfoInToken
    expires_at: datetime