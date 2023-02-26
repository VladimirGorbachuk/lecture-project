from abc import abstractmethod
from typing import Any

from pydantic import BaseModel

from domain.auth import UserAuthenticationInfo, UserInfoInToken, UserRegistrationInfo
from .base import ConvertableToEntity


class UserRegistrationInfoSerializer(ConvertableToEntity):
    login: str
    email: str

    def to_entity(self) -> UserRegistrationInfo:
        return UserRegistrationInfo(**self.dict())


class UserAuthenticationInfoSerializer(ConvertableToEntity):
    login: str
    password: str

    def to_entity(self) -> UserAuthenticationInfo:
        return UserAuthenticationInfo(**self.dict())


class UserInfoInTokenSerializer(BaseModel):
    login: str
    email: str

    def to_entity(self) -> UserInfoInToken:
        return UserInfoInToken(**self.dict())