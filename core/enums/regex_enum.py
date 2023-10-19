from enum import Enum


class RegExEnum(Enum):
    NAME = (
        r'^[a-zа-яёіA-ZА-ЯЇЁ]+$',
        'First letter uppercase min 2 max 20 ch'
    )
    PHONE = (
        r'^\d{12}$',
        'Phone number must be 12 digits'
    )
    GROUP = (
        r'^[a-zA-Z0-9\-]+$',
        'The group name must contain letters and numbers'
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
