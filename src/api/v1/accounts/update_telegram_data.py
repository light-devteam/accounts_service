from uuid import UUID

from fastapi import status

from src.api.v1.accounts.router import router
from src.schemas import UpdateTelegramDataSchema
from src.services import AccountsService


@router.patch(
    '/{account_id}/update_tg_data',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_telegram_data(
    account_id: UUID,
    update_data: UpdateTelegramDataSchema,
) -> None:
    await AccountsService.update_telegram_data(
        account_id,
        update_data.first_name,
        update_data.last_name,
        update_data.username,
    )
