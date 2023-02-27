from dataclasses import dataclass
import os


@dataclass
class AuthServiceSettings:
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


def configure_auth() -> AuthServiceSettings:
    return AuthServiceSettings(
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