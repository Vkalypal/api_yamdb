from django.core.exceptions import ValidationError
from django.utils import timezone


def NotLaterThisYearValidator(value):
    if value > timezone.now().year:
        raise ValidationError(
            (f'Год выхода {value} не может быть позже текущего года!'),
            params={'value': value},
        )
