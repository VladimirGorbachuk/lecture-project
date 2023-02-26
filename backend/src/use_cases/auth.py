from datetime import datetime, timedelta
from typing import Any, Protocol, TypeVar

from domain.auth import AuthToken, UserInfoInToken
from exceptions.auth import AccessTokenExpiredException, RefreshTokenExpiredException
from service_intefaces.auth import (
    AuthSettings,
    TokenFromRequestCookieGetterInterface,
    TokenToResponseCookieSetterInterface,
    TokenFromResponseCookieRemoverInterface,
)


T = TypeVar("T")


class AuthenticatorProtocol(Protocol):
    auth_settings: AuthSettings
    token_from_request_cookie_getter: TokenFromRequestCookieGetterInterface
    token_to_response_cookie_setter: TokenToResponseCookieSetterInterface
    token_from_response_cookie_remover: TokenFromResponseCookieRemoverInterface

    def set_auth_tokens(self, response: T, auth_info: UserInfoInToken) -> T:
        raise NotImplementedError

    def _set_access_token(self, response: T, auth_info: UserInfoInToken) -> T:
        raise NotImplementedError

    def _set_refresh_token(self, response: T, auth_info: UserInfoInToken) -> T:
        raise NotImplementedError

    def check_access_token(self, request: Any) -> bool:
        raise NotImplementedError

    def check_refresh_token(self, request: Any) -> bool:
        raise NotImplementedError
  
    def refresh_access_token(self, request: Any, response: T) -> T:
        raise NotImplementedError
 
    def revoke_token(self, response: T) -> T:
        raise NotImplementedError
    
    def get_auth_info_from_token(self, request: Any) -> UserInfoInToken:
        raise NotImplementedError


class Authenticator:
    def __init__(
        self,
        auth_settings: AuthSettings,
        token_from_request_cookie_getter: TokenFromRequestCookieGetterInterface,
        token_to_response_cookie_setter: TokenToResponseCookieSetterInterface,
        token_from_response_cookie_remover: TokenFromResponseCookieRemoverInterface,
    ):
        self.auth_settings = auth_settings
        self.token_from_request_cookie_getter = token_from_request_cookie_getter
        self.token_to_response_cookie_setter = token_to_response_cookie_setter
        self.token_from_response_cookie_remover = token_from_response_cookie_remover

    def set_auth_tokens(self, response: T, auth_info: UserInfoInToken) -> T:
        user_info = UserInfoInToken(login=auth_info.login, email=auth_info.email)
        access_token_expires_at = datetime.now() + timedelta(seconds=self.auth_settings.AUTH_TOKEN_LIFETIME_SECONDS)
        access_token_info = AuthToken(data=user_info, expires_at=access_token_expires_at)
        response_with_access_token = self.token_to_response_cookie_setter.set_access_token_to_response(
            response,
            token_info=access_token_info,
        )
        refresh_token_expires_at = datetime.now() + timedelta(seconds=self.auth_settings.REFRESH_TOKEN_LIFETIME_SECONDS)
        refresh_token_info = AuthToken(data=user_info, expires_at=refresh_token_expires_at)
        response_with_both_tokens = self.token_to_response_cookie_setter.set_refresh_token_to_response(
            response_with_access_token,
            token_info=refresh_token_info,
        )
        return response_with_both_tokens

    def _set_access_token(self, response: T, auth_info: UserInfoInToken) -> T:
        user_info = UserInfoInToken(login=auth_info.login, email=auth_info.email)
        access_token_expires_at = datetime.now() + timedelta(seconds=self.auth_settings.AUTH_TOKEN_LIFETIME_SECONDS)
        access_token_info = AuthToken(data=user_info, expires_at=access_token_expires_at)
        return self.token_to_response_cookie_setter.set_access_token_to_response(
            response,
            token_info=access_token_info,
        )
    
    def _set_refresh_token(self, response: T, auth_info: UserInfoInToken) -> T:
        user_info = UserInfoInToken(login=auth_info.login, email=auth_info.email)
        refresh_token_expires_at = datetime.now() + timedelta(seconds=self.auth_settings.REFRESH_TOKEN_LIFETIME_SECONDS)
        refresh_token_info = AuthToken(data=user_info, expires_at=refresh_token_expires_at)
        return self.token_to_response_cookie_setter.set_refresh_token_to_response(
            response,
            token_info=refresh_token_info,
        )

    def check_access_token(self, request: Any) -> bool:
        access_token = self.token_from_request_cookie_getter.get_access_token_from_request(request)
        if access_token.expires_at >= datetime.now():
            return True
        raise AccessTokenExpiredException

    def check_refresh_token(self, request: Any) -> bool:
        refresh_token = self.token_from_request_cookie_getter.get_refresh_token_from_request(request)
        if refresh_token.expires_at >= datetime.now():
            return True
        return False
  
    def refresh_access_token(self, request: Any, response: T) -> T:
        if self.check_refresh_token(request):
            return self._set_access_token(response)
        else:
            raise RefreshTokenExpiredException
 
    def revoke_token(self, response: T) -> T:
        """should consider blacklisting the token"""
        return self.token_from_response_cookie_remover.remove_auth_tokens_from_cookies(response)
    
    def get_auth_info_from_token(self, request: Any) -> UserInfoInToken:
        access_token = self.token_from_request_cookie_getter.get_access_token_from_request(request)
        if access_token.expires_at >= datetime.now():
            return access_token.data
        raise AccessTokenExpiredException
        