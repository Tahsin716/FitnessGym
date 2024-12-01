from dataclasses import dataclass

from src.models.entities.base_entity import BaseEntity


@dataclass
class Member(BaseEntity):
    def __init__(self):
        super().__init__()
