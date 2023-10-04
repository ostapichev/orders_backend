from dataclasses import dataclass
from datetime import datetime

from core.dataclasses.group_dataclasses import GroupDataClass
from core.dataclasses.user_dataclass import ProfileDataClass


@dataclass
class OrderDataClass:
    id: int
    name: str
    surname: str
    email: str
    phone: int
    age: int
    course: str
    course_format: str
    course_type: str
    already_paid: int
    sum: int
    utm: str
    msg: str
    status: str
    group_id: GroupDataClass
    manager_id: ProfileDataClass
    created_at: datetime
    updated_at: datetime
