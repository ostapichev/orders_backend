from enum import Enum


class RegExEnum(Enum):
    BASE_NAME_PATTERN = (
        r'^[a-zA-Zа-яА-яёЁіІїЇ]{2,20}$',
        'First letter uppercase min 2 max 20 ch'
    )
    PHONE = (
        r'^\d{12}$',
        'Phone number must be 12 digits'
    )
    GROUP = (
        r'^[a-z]{3}-\d{4}$',
        'Only special format group. For example: dec-2023'
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
