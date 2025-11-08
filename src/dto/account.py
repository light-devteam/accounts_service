from uuid import UUID

from msgspec import Struct


class AccountDTO(Struct):
    id: UUID
    telegram_id: int
    username: str | None
    first_name: str
    last_name: str
    created_at: int
    updated_at: int
