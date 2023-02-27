from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Contact:
    type: str
    info: str
    link: str


@dataclass
class CurriculumVitae:
    id: int
    title: str
    text: str
    image_path: str


@dataclass
class User:
    login: str
    email: str
    contact_info: "list[Contact]"
    whitelist: "list[str]"
    blacklist: "list[str]"
    curricullum_vitae_id: Optional[int] = None


