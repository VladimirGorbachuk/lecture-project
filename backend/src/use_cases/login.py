from abc import abstractmethod
from typing import Protocol

from domain.auth import UserAuthenticationInfo
from domain.user import User
from exceptions.auth import WrongUserCredentialsException
from service_intefaces.auth import LoginInterface


class LoginManagerProtocol(Protocol):
    login_service: LoginInterface
    
    @abstractmethod
    def login(self, user_auth_info: UserAuthenticationInfo) -> User:
        raise NotImplementedError
    

class LoginManager(LoginManagerProtocol):
    def __init__(self, login_service: LoginInterface):
        self.login_service = login_service
    
    def login(self, user_auth_info: UserAuthenticationInfo) -> User:
        return self.login_service.login(user_auth_info)
    