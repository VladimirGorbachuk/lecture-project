import os

from fastapi import Depends, FastAPI

from service_intefaces.auth import (
    AuthSettings,
    TokenFromRequestCookieGetterInterface,
    TokenFromResponseCookieRemoverInterface,
    TokenToResponseCookieSetterInterface,
    TokenEncoderInterface,
    TokenDecoderInterface,
)
from service_implementations.auth_cookie import (
    TokenEncoder,
    TokenDecoder,
    TokenGetterFromFastApiRequest,
    TokenRemoverFromFastApiResponse,
    TokenCookieSetterForFastAPIResponse,
)
from use_cases.auth import AuthenticatorProtocol, Authenticator


def configure_auth() -> AuthSettings:
    return AuthSettings(
        AUTH_TOKEN_LIFETIME_SECONDS=float(os.environ["AUTH_TOKEN_LIFETIME_SECONDS"]),
        REFRESH_TOKEN_LIFETIME_SECONDS=float(os.environ["REFRESH_TOKEN_LIFETIME_SECONDS"]),
        AUTH_SECRET_KEY=os.environ["AUTH_SECRET_KEY"],
        ENCODING_ALGORITHM=os.environ["ENCODING_ALGORITHM"],
        SECURE_COOKIE=os.environ["SECURE_COOKIE"]=="True",
        REFRESH_TOKEN_KEY="refresh_token",
        ACCESS_TOKEN_KEY="access_token",
        HTTP_ONLY_COOKIE=os.environ["HTTP_ONLY_COOKIE"]=="True",
        AUTH_TOKEN_IN_COOKIES=os.environ["AUTH_TOKEN_IN_COOKIES"]=="True",
        AUTH_TOKEN_CSRF_PROTECT=os.environ["AUTH_TOKEN_CSRF_PROTECT"]=="True",
    )


def initialize_authenticator() -> Authenticator:
    auth_settings=configure_auth()
    token_decoder=TokenDecoder(auth_settings)
    token_encoder=TokenEncoder(auth_settings)
    token_from_request_cookie_getter=TokenGetterFromFastApiRequest(auth_settings, token_decoder=token_decoder)
    token_from_response_cookie_remover=TokenRemoverFromFastApiResponse(auth_settings)
    token_to_response_cookie_setter=TokenCookieSetterForFastAPIResponse(auth_settings, token_encoder=token_encoder)
    return Authenticator(
        auth_settings=auth_settings,
        token_from_request_cookie_getter=token_from_request_cookie_getter,
        token_from_response_cookie_remover=token_from_response_cookie_remover,
        token_to_response_cookie_setter=token_to_response_cookie_setter,
    )


def bind_token_implementations_to_fastapi(app: FastAPI) -> FastAPI:

    app.dependency_overrides[AuthSettings] = lambda: configure_auth()
    app.dependency_overrides[AuthenticatorProtocol] = lambda: initialize_authenticator()
    # app.dependency_overrides[TokenFromRequestCookieGetterInterface] = lambda: TokenGetterFromFastApiRequest(
    #     settings=Depends(AuthSettings),
    #     token_decoder=Depends(TokenDecoderInterface),
    # )
    # app.dependency_overrides[TokenFromResponseCookieRemoverInterface] = lambda: TokenRemoverFromFastApiResponse(
    #     settings=Depends(AuthSettings),
    # )
    # app.dependency_overrides[TokenToResponseCookieSetterInterface] = lambda: TokenCookieSetterForFastAPIResponse(
    #     settings=Depends(AuthSettings),
    #     token_encoder=Depends(TokenEncoderInterface),
    # )
    # app.dependency_overrides[TokenEncoderInterface] = lambda: TokenEncoder(auth_settings=Depends(AuthSettings))
    # app.dependency_overrides[TokenDecoderInterface] = lambda: TokenDecoder(auth_settings=Depends(AuthSettings))
    # app.dependency_overrides[AuthenticatorProtocol] = lambda: Authenticator(
    #     auth_settings=Depends(AuthSettings),
    #     token_from_request_cookie_getter=Depends(TokenFromRequestCookieGetterInterface),
    #     token_from_response_cookie_remover=Depends(TokenFromResponseCookieRemoverInterface),
    #     token_to_response_cookie_setter=Depends(TokenToResponseCookieSetterInterface),
    # )
    return app