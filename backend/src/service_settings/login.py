from dataclasses import dataclass
import os


@dataclass
class LoginServiceSettings:
    PASSWORD_ENCRYPTION_KEY: str


def configure_login() -> LoginServiceSettings:
    return LoginServiceSettings(
        PASSWORD_ENCRYPTION_KEY=os.environ["PASSWORD_ENCRYPTION_KEY"],
    )