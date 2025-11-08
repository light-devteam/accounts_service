from enum import StrEnum


class RegistrationMode(StrEnum):
    ALLOW = 'ALLOW'
    STRICT = 'STRICT'
    DENY = 'DENY'
