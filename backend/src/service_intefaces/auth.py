from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, TypeVar

from domain.auth import (
    AuthenticationCasesEnum,
    AuthToken, 
    UserAuthenticationInfo,
    UserInfoInToken,
    UserRegistrationInfo,
)
from domain.user import User
from service_settings.auth import AuthServiceSettings
from service_settings.login import LoginServiceSettings


T = TypeVar("T")


class LoginInterface(Protocol):
    settings: LoginServiceSettings

    @abstractmethod
    def login(self, user_auth_info: UserAuthenticationInfo) -> User:
        raise NotImplementedError


class RegisterInterface(Protocol):
    settings: AuthServiceSettings

    @abstractmethod
    def register(self, user_registration_info: UserRegistrationInfo) -> bool:
        raise NotImplementedError


class TokenEncoderInterface(Protocol):
    settings: AuthServiceSettings

    @abstractmethod
    def encode_access_token(self, user_info: UserInfoInToken) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def encode_refresh_token(self, user_info: UserInfoInToken) -> str:
        raise NotImplementedError


class TokenDecoderInterface(Protocol):
    settings: AuthServiceSettings

    @abstractmethod
    def decode_access_token(self, token_encoded_str: str) -> UserInfoInToken:
        raise NotImplementedError
    
    @abstractmethod
    def decode_refresh_token(self, token_encoded_str: str) -> UserInfoInToken:
        raise NotImplementedError


class TokenToResponseCookieSetterInterface(Protocol):
    settings: AuthServiceSettings
    token_encoder: TokenEncoderInterface

    def set_access_token_to_response(self, response: T, user_info: UserInfoInToken) -> T:
        raise NotImplementedError

    def set_refresh_token_to_response(self, response: T, user_info: UserInfoInToken) -> T:
        raise NotImplementedError


class TokenFromRequestCookieGetterInterface(Protocol):
    settings: AuthServiceSettings
    token_decoder: TokenDecoderInterface

    def get_access_token_from_request(self, request: Any) -> UserInfoInToken:
        raise NotImplementedError

    def get_refresh_token_from_request(self, request: Any) -> UserInfoInToken:
        raise NotImplementedError



class TokenFromResponseCookieRemoverInterface(Protocol):
    settings: AuthServiceSettings

    def remove_auth_tokens_from_cookies(self, response: T, token_info: UserInfoInToken) -> T:
        raise NotImplementedError
