from src.api.v1.referral_codes.router import router
from src.api.v1.referral_codes.create import router
from src.api.v1.referral_codes.get import router
from src.api.v1.referral_codes.set_available import router
from src.api.v1.referral_codes.set_unavailable import router
from src.api.v1.referral_codes.get_account_codes import router


__all__ = [
    'router'
]
