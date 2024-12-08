import os


class Config:
    DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data_layer/db"))
    DB_NAME = "fitness_gym.json"