from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, field_serializer


class AccountSchema(BaseModel):
    id: UUID
    telegram_id: int
    username: Optional[str] = None
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

    @field_serializer(
        'created_at',
        'updated_at',
        when_used='json-unless-none',
    )
    def serialize_datetime(self, value: datetime) -> float:
        return value.timestamp()
