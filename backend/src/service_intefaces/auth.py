from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol, TypeVar

from domain.auth import AuthenticationCasesEnum, AuthToken, UserAuthenticationInfo, UserRegistrationInfo


T = TypeVar("T")


@dataclass
class AuthSettings:
    AUTH_TOKEN_LIFETIME_SECONDS: float
    REFRESH_TOKEN_LIFETIME_SECONDS: float
    AUTH_SECRET_KEY: str
    AUTH_TOKEN_IN_COOKIES: bool
    AUTH_TOKEN_CSRF_PROTECT: bool
    HTTP_ONLY_COOKIE: bool = True
    SECURE_COOKIE: bool = False
    ACCESS_TOKEN_KEY: str = "access_token"
    REFRESH_TOKEN_KEY: str = "refresh_token"
    ENCODING_ALGORITHM: str = "HS512"
    

class LoginInterface(Protocol):
    settings: AuthSettings

    @abstractmethod
    def login(self, user_auth_info: UserAuthenticationInfo) -> bool:
        raise NotImplementedError


class RegisterInterface(Protocol):
    settings: AuthSettings

    @abstractmethod
    def register(self, user_registration_info: UserRegistrationInfo) -> bool:
        raise NotImplementedError


class TokenEncoderInterface(Protocol):
    settings: AuthSettings

    @abstractmethod
    def encode_access_token(self, token_info: AuthToken) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def encode_refresh_token(self, token_info: AuthToken) -> str:
        raise NotImplementedError


class TokenDecoderInterface(Protocol):
    settings: AuthSettings

    @abstractmethod
    def decode_access_token(self, token_encoded_str: str) -> AuthToken:
        raise NotImplementedError
    
    @abstractmethod
    def decode_refresh_token(self, token_encoded_str: str) -> AuthToken:
        raise NotImplementedError


class TokenToResponseCookieSetterInterface(Protocol):
    settings: AuthSettings
    token_encoder: TokenEncoderInterface

    def set_access_token_to_response(self, response: T, token_info: AuthToken) -> T:
        raise NotImplementedError

    def set_refresh_token_to_response(self, response: T, token_info: AuthToken) -> T:
        raise NotImplementedError


class TokenFromRequestCookieGetterInterface(Protocol):
    settings: AuthSettings
    token_decoder: TokenDecoderInterface

    def get_access_token_from_request(self, request: Any) -> AuthToken:
        raise NotImplementedError

    def get_refresh_token_from_request(self, request: Any) -> AuthToken:
        raise NotImplementedError



class TokenFromResponseCookieRemoverInterface(Protocol):
    settings: AuthSettings

    def remove_auth_tokens_from_cookies(self, response: T, token_info: AuthToken) -> T:
        raise NotImplementedError
