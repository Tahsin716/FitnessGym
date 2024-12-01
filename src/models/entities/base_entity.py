from dataclasses import dataclass
import datetime
from src.models.utils.common import Common


@dataclass
class BaseEntity:
    def __init__(self):
        self.__id: str = Common.new_guid()
        self.__create_date: datetime = datetime.datetime.now(datetime.timezone.utc)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def create_date(self) -> datetime:
        return self.__create_date