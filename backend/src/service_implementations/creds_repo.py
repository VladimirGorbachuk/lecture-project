from domain.auth import UserAuthenticationInfo
from domain.user import User
from exceptions.auth import WrongUserCredentialsException
from service_intefaces.auth import LoginInterface
from service_settings.login import LoginServiceSettings


class LoginStub(LoginInterface):
    def __init__(self, settings: LoginServiceSettings):
        self.settings = settings

    def login(self, user_auth_info: UserAuthenticationInfo) -> User:
        if user_auth_info.login == "test" and user_auth_info.password == "test":
            return User(
                login="test",
                email="test@test.test",
                contact_info=[],
                whitelist=[],
                blacklist=[],
                curricullum_vitae_id=None,
            )
        else:
            raise WrongUserCredentialsException("provided login and/or password are wrong")