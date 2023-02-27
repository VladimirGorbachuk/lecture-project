import os

from fastapi import Depends, FastAPI

from service_intefaces.auth import (
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
from service_implementations.creds_repo import LoginStub
from service_settings.auth import AuthServiceSettings, configure_auth
from service_settings.login import LoginServiceSettings, configure_login
from use_cases.auth import AuthenticatorProtocol, Authenticator
from use_cases.login import LoginManager, LoginManagerProtocol


def initialize_authenticator() -> Authenticator:
    auth_settings=configure_auth()
    token_decoder=TokenDecoder(auth_settings)
    token_encoder=TokenEncoder(auth_settings)
    token_from_request_cookie_getter=TokenGetterFromFastApiRequest(auth_settings, token_decoder=token_decoder)
    token_from_response_cookie_remover=TokenRemoverFromFastApiResponse(auth_settings)
    token_to_response_cookie_setter=TokenCookieSetterForFastAPIResponse(auth_settings, token_encoder=token_encoder)
    return Authenticator(
        token_from_request_cookie_getter=token_from_request_cookie_getter,
        token_from_response_cookie_remover=token_from_response_cookie_remover,
        token_to_response_cookie_setter=token_to_response_cookie_setter,
    )


def initialize_login_manager() -> LoginManager:
    login_settings = configure_login()
    login_service = LoginStub(login_settings)
    return LoginManager(login_service=login_service)


def bind_token_implementations_to_fastapi(app: FastAPI) -> FastAPI:

    app.dependency_overrides[AuthServiceSettings] = lambda: configure_auth()
    app.dependency_overrides[AuthenticatorProtocol] = lambda: initialize_authenticator()
    app.dependency_overrides[LoginManagerProtocol] = lambda: initialize_login_manager()

    return app