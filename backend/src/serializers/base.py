from abc import abstractmethod
from typing import Any

from pydantic import BaseModel


class ConvertableToEntity(BaseModel):
    @abstractmethod
    def to_entity(self) -> Any:
        raise NotImplementedError