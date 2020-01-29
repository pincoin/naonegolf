from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class DailyBooking(model_utils_models.TimeStampedModel):
    day = models.DateField(
        verbose_name=_('Day'),
        db_index=True,
        unique=True,
    )

    class Meta:
        verbose_name = _('Daily booking')
        verbose_name_plural = _('Daily bookings')

    def __str__(self):
        return '{}'.format(self.day)


class TeeOffTime(model_utils_models.TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'open', _('Open')),
        (1, 'held', _('Held')),
        (2, 'held', _('Closed')),
    )

    day = models.ForeignKey(
        'windmill.DailyBooking',
        verbose_name=_('Booking day'),
        on_delete=models.CASCADE,
    )

    hour = models.IntegerField(
        validators=[
            validators.MaxValueValidator(6),
            validators.MinValueValidator(19)
        ]
    )

    minute = models.IntegerField(
        validators=[
            validators.MaxValueValidator(0),
            validators.MinValueValidator(59)
        ]
    )

    class Meta:
        verbose_name = _('Daily tee off time')
        verbose_name_plural = _('Daily tee off times')

        unique_together = ('day', 'hour', 'minute')
