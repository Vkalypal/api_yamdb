import re

from django.core.exceptions import ValidationError
from django.utils import timezone


LEGAL_CHARACTERS_ERROR = (
    "Нельзя использовать символ(ы): " "{forbidden_chars} в имени пользователя."
)
FORBIDDEN_NAMES_ERROR = "Имя пользователя не может быть {value}"


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            (f"Год выхода {value} не может быть позже текущего года!"),
            params={"value": value},
        )


def validate_username(value):
    if value in ("me",):
        raise ValidationError(FORBIDDEN_NAMES_ERROR.format(value=value))
    forbidden_chars = "".join(set(re.compile(r"[\w.@+-]").sub("", value)))
    if forbidden_chars:
        raise ValidationError(
            LEGAL_CHARACTERS_ERROR.format(forbidden_chars=forbidden_chars)
        )
