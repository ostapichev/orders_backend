from dataclasses import dataclass
from datetime import datetime


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
    group_id: int
    manager_id: int
    created_at: datetime
    updated_at: datetime
