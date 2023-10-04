from dataclasses import dataclass
from datetime import datetime

from core.dataclasses.order_dataclass import OrderDataClass
from core.dataclasses.user_dataclass import ProfileDataClass


@dataclass
class CommentDataClass:
    id: int
    comment: str
    order: OrderDataClass
    profile: ProfileDataClass
    created_at: datetime
    updated_at: datetime
