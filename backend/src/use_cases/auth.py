from datetime import datetime, timedelta
from typing import Any, Protocol, TypeVar

from domain.auth import AuthToken, UserInfoInToken
from exceptions.auth import AccessTokenExpiredException, RefreshTokenExpiredException
from service_intefaces.auth import (
    TokenFromRequestCookieGetterInterface,
    TokenToResponseCookieSetterInterface,
    TokenFromResponseCookieRemoverInterface,
)


T = TypeVar("T")


# TODO: should consider using separate settings for use cases or using them ONLY for services


class AuthenticatorProtocol(Protocol):
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


class Authenticator:
    def __init__(
        self,
        token_from_request_cookie_getter: TokenFromRequestCookieGetterInterface,
        token_to_response_cookie_setter: TokenToResponseCookieSetterInterface,
        token_from_response_cookie_remover: TokenFromResponseCookieRemoverInterface,
    ):
        self.token_from_request_cookie_getter = token_from_request_cookie_getter
        self.token_to_response_cookie_setter = token_to_response_cookie_setter
        self.token_from_response_cookie_remover = token_from_response_cookie_remover

    def set_auth_tokens(self, response: T, auth_info: UserInfoInToken) -> T:
        # TODO: consider using self._set_access_token and self._set_refresh_token
        # TODO: should we keep this expiration logic in services? 
        response_with_access_token = self.token_to_response_cookie_setter.set_access_token_to_response(
            response,
            user_info=auth_info,
        )
        response_with_both_tokens = self.token_to_response_cookie_setter.set_refresh_token_to_response(
            response_with_access_token,
            user_info=auth_info,
        )
        return response_with_both_tokens

    def check_access_token(self, request: Any) -> bool:
        try:
            self.token_from_request_cookie_getter.get_access_token_from_request(request)
            return True
        except AccessTokenExpiredException:
            return False

    def check_refresh_token(self, request: Any) -> bool:
        try:
            self.token_from_request_cookie_getter.get_refresh_token_from_request(request)
            return True
        except RefreshTokenExpiredException:
            return False
  
    def refresh_access_token(self, request: Any, response: T) -> T:
        user_info = self.token_from_request_cookie_getter.get_refresh_token_from_request(request)
        return self.token_to_response_cookie_setter.set_access_token_to_response(
            response,
            user_info=user_info,
        )
 
    def revoke_token(self, response: T) -> T:
        """should consider blacklisting the token"""
        return self.token_from_response_cookie_remover.remove_auth_tokens_from_cookies(response)
        