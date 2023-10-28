from datetime import timedelta
from enum import Enum


class ActionTokenEnum(Enum):
    ACTIVATE = (
        'activate',
        timedelta(minutes=1)
    )
    RECOVERY = (
        'recovery',
        timedelta(minutes=2)
    )

    def __init__(self, token_type, life_time):
        self.token_type = token_type
        self.life_time = life_time
