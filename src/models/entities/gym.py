import datetime
from typing import Dict


class Gym:
    def __init__(self, data : Dict):
        self.__id : str = 'guid'
        self.create_date : datetime = datetime.datetime.now(datetime.timezone.utc)
        self.__post_code : str = data['post_code']
        self.__address : str = data['address']
        self.__contact_number : str = data['contact_number']
        self.__email : str = data['email']

