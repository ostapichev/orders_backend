from dataclasses import dataclass
from datetime import datetime


@dataclass
class GroupDataClass:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
