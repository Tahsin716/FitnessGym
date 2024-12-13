from src.data_layer.entities.base_entity import BaseEntity


class Attendance(BaseEntity):
    def __init__(self, data : dict):
        _id = data.get('_id', None)
        create_date = data.get('create_date', None)
        super().__init__(_id, create_date)

        self.__member_id : str = data['member_id']
        self.__gym_id : str = data['gym_id']
        self.__zone_id : str = data['zone_id']
        self.__checkin_time : str = data['checkin_time']
        self.__checkout_time : str = data['checkout_time']
        self.__duration : int = data['duration']

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def gym_id(self) -> str:
        return self.__gym_id

    @property
    def zone_id(self) -> str:
        return self.__zone_id

    @property
    def checkin_time(self) -> str:
        return self.__checkin_time

    @property
    def checkout_time(self) -> str:
        return self.__checkout_time

    @property
    def duration(self) -> int:
        return self.__duration