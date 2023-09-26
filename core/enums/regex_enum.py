from enum import Enum


class RegExEnum(Enum):
    NAME = (
        r'^[a-zа-яёіA-ZА-ЯЇЁ]+$',
        'First letter uppercase min 2 max 35 ch'
    )
    PASSWORD = (
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=(?:.*[`~!@#$%^&*()\-_+=\\\|\'\"\;\:\/?.>,<\[\]\{\}]){2,'
        r'})[a-zA-Z\d`~!@#$%^&*()\-_+=\\\|\'\"\;\:\/?.>,<\[\]\{\}]{8,30}$',
        [
            'min 1 lowercase ch',
            'min 1 uppercase ch',
            'min 1 digit',
            'min 1 special character',
            'length 8-30'
        ]
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
