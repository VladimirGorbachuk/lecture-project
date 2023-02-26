class BaseAuthTokenException(Exception):
    pass


class TokenExpiredException(BaseAuthTokenException):
    pass


class TokenInvalidException(BaseAuthTokenException):
    pass


class AccessTokenExpiredException(TokenExpiredException):
    pass


class RefreshTokenExpiredException(TokenExpiredException):
    pass


class CookieWithTokenIsMissingException(BaseAuthTokenException):
    pass
