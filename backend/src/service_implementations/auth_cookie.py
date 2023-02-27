from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TypedDict

from fastapi import Response, Request
import jwt

from domain.auth import AuthToken, UserInfoInToken
from exceptions.auth import AccessTokenExpiredException, RefreshTokenExpiredException, TokenInvalidException, CookieWithTokenIsMissingException
from service_intefaces.auth import (
    TokenFromRequestCookieGetterInterface,
    TokenToResponseCookieSetterInterface,
    TokenFromResponseCookieRemoverInterface,
    TokenEncoderInterface,
    TokenDecoderInterface,
)
from service_settings.auth import AuthServiceSettings


class JwtPayloadToEncode(TypedDict):
    email: str
    login: str
    exp: datetime


class JwtPayloadDecoded(TypedDict):
    email: str
    login: str
    exp: int


class TokenEncoder(TokenEncoderInterface):
    def __init__(self, settings: AuthServiceSettings):
        self.settings = settings

    def encode_access_token(self, user_info: UserInfoInToken) -> str:
        access_token_expires_at = datetime.now() + timedelta(seconds=self.settings.AUTH_TOKEN_LIFETIME_SECONDS)
        token_info = AuthToken(data=user_info, expires_at=access_token_expires_at)
        payload = JwtPayloadToEncode(
            email=token_info.data.email,
            login=token_info.data.login,
            exp=token_info.expires_at,
        )
        return jwt.encode(
            payload,
            self.settings.AUTH_SECRET_KEY,
            algorithm = self.settings.ENCODING_ALGORITHM,
        )
    
    def encode_refresh_token(self, user_info: UserInfoInToken) -> str:
        refresh_token_expires_at = datetime.now() + timedelta(seconds=self.settings.REFRESH_TOKEN_LIFETIME_SECONDS)
        token_info = AuthToken(data=user_info, expires_at=refresh_token_expires_at)
        payload = JwtPayloadToEncode(
            email=token_info.data.email,
            login=token_info.data.login,
            exp=token_info.expires_at,
        )
        return jwt.encode(
            payload,
            self.settings.AUTH_SECRET_KEY,
            algorithm = self.settings.ENCODING_ALGORITHM,
        )


class TokenDecoder(TokenDecoderInterface):
    def __init__(self, settings: AuthServiceSettings):
        self.settings = settings

    def decode_access_token(self, token_encoded_str: str) -> UserInfoInToken:
        payload: JwtPayloadDecoded = jwt.decode(
            token_encoded_str,
            self.settings.AUTH_SECRET_KEY,
            algorithms=[self.settings.ENCODING_ALGORITHM],
        )
        expires_at = datetime.fromtimestamp(payload["exp"])
        if expires_at >= datetime.now():
            raise AccessTokenExpiredException("Access token has been expired")
        return UserInfoInToken(email=payload["email"], login=payload["login"])


    def decode_refresh_token(self, token_encoded_str: str) -> UserInfoInToken:
        payload: JwtPayloadDecoded = jwt.decode(
            token_encoded_str,
            self.settings.AUTH_SECRET_KEY,
            algorithms=[self.settings.ENCODING_ALGORITHM],
        )
        expires_at = datetime.fromtimestamp(payload["exp"])
        if expires_at >= datetime.now():
            raise RefreshTokenExpiredException("Refresh token has been expired")
        return UserInfoInToken(email=payload["email"], login=payload["login"])



class TokenCookieSetterForFastAPIResponse(TokenToResponseCookieSetterInterface):
    def __init__(self, settings: AuthServiceSettings, token_encoder: TokenEncoderInterface):
        self.settings = settings
        self.token_encoder = token_encoder
    
    def set_access_token_to_response(self, response: Response, user_info: UserInfoInToken) -> Response:
        encoded_token = self.token_encoder.encode_access_token(user_info)
        response.set_cookie(
            key=self.settings.ACCESS_TOKEN_KEY,
            value=encoded_token,
            httponly=self.settings.HTTP_ONLY_COOKIE,
            samesite="lax",
        )
        return response

    def set_refresh_token_to_response(self, response: Response, user_info: UserInfoInToken) -> Response:
        encoded_token = self.token_encoder.encode_refresh_token(user_info)
        response.set_cookie(
            key=self.settings.REFRESH_TOKEN_KEY,
            value=encoded_token,
        )
        return response


class TokenGetterFromFastApiRequest(TokenFromRequestCookieGetterInterface):
    def __init__(self, settings: AuthServiceSettings, token_decoder: TokenDecoderInterface):
        self.settings = settings
        self.token_decoder = token_decoder

    def get_access_token_from_request(self, request: Request) -> AuthToken:
        access_cookie = request.cookies.get(self.settings.ACCESS_TOKEN_KEY)
        if not access_cookie:
            raise CookieWithTokenIsMissingException
        try:
            return self.token_decoder.decode_access_token(access_cookie)
        except jwt.exceptions.InvalidSignatureError:
            raise TokenInvalidException

    def get_refresh_token_from_request(self, request: Request) -> AuthToken:
        refresh_cookie = request.cookies.get(self.settings.REFRESH_TOKEN_KEY)
        if not refresh_cookie:
            raise CookieWithTokenIsMissingException
        try:
            return self.token_decoder.decode_refresh_token(refresh_cookie)
        except jwt.exceptions.InvalidSignatureError:
            raise TokenInvalidException



class TokenRemoverFromFastApiResponse(TokenFromResponseCookieRemoverInterface):
    def __init__(self, settings: AuthServiceSettings):
        self.settings = settings

    def remove_auth_tokens_from_cookies(self, response: Response) -> Response:
        response.delete_cookie(self.settings.ACCESS_TOKEN_KEY)
        response.delete_cookie(self.settings.REFRESH_TOKEN_KEY)
        return response