import datetime


from src.data_layer.utils.common import Common


class BaseEntity:
    def __init__(self, _id : str = None, create_date : str = None):
        self.__id: str = Common.new_guid() if _id is None else _id
        self.__create_date: datetime = datetime.datetime.now(datetime.timezone.utc) if create_date is None else datetime.datetime.strptime(create_date, '%Y-%m-%d')

    @property
    def id(self) -> str:
        return self.__id

    @property
    def create_date(self) -> datetime:
        return self.__create_date