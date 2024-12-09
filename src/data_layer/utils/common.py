from uuid import uuid4


class Common:

    @staticmethod
    def new_guid() -> str:
        return str(uuid4()).split('-')[0]