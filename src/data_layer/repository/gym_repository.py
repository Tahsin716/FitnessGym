from src.data_layer.entities.gym import Gym


class GymRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__gyms = {}
        return cls._instance

    def create_gym(self, data: dict) -> Gym:
        gym = Gym(data)
        self.__gyms[gym.id] = gym
        return gym

    def update_gym(self, _id: str, data: dict) -> Gym:
        gym = self.__gyms[_id]
        gym.post_code = data['post_code']
        gym.address = data['address']
        gym.contact_number = data['contact_number']
        gym.email = data['email']
        return gym

    def get_all_gyms(self) -> list[Gym]:
        return list(self.__gyms.values())

    def get_gym_by_id(self, _id: str) -> Gym:
        return self.__gyms.get(_id)

    def remove_gym(self, _id: str):
        if _id in self.__gyms:
            del self.__gyms[_id]