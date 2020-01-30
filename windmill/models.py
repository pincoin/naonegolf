from django.conf import settings
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class BookingOrder(model_utils_models.TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Customer'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )


class Booking(model_utils_models.TimeStampedModel):
    order = models.ForeignKey(
        'windmill.BookingOrder',
        verbose_name=_('Booking order'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.CASCADE,
    )

    daily_booking = models.ForeignKey(
        'windmill.DailyBooking',
        verbose_name=_('Daily booking'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.CASCADE,
    )


class Golfer(model_utils_models.TimeStampedModel):
    booking = models.ForeignKey(
        'windmill.Booking',
        verbose_name=_('Daily booking'),
        on_delete=models.CASCADE,
    )


class DailyBooking(model_utils_models.TimeStampedModel):
    day = models.DateField(
        verbose_name=_('Booking Day'),
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
        verbose_name=_('Tee off hour'),
        validators=[
            validators.MinValueValidator(6),
            validators.MaxValueValidator(19),
        ]
    )

    minute = models.IntegerField(
        verbose_name=_('Tee off minute'),
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(59),
        ]
    )

    status = models.IntegerField(
        verbose_name=_('Tee off status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.open,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Daily tee off time')
        verbose_name_plural = _('Daily tee off times')

        unique_together = ('day', 'hour', 'minute')
