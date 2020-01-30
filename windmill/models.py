from decimal import Decimal

from django.conf import settings
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class BookingOrder(model_utils_models.TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'order_opened', _('order opened')),
        (1, 'order_pending', _('order pending')),
        (2, 'payment_pending', _('payment pending')),
        (3, 'completed', _('order complete')),
        (4, 'offered', _('order offered')),
        (5, 'voided', _('order voided')),
        (6, 'refund_requested', _('refund requested')),
        (7, 'refund_pending', _('refund pending')),
        (8, 'refunded1', _('order refunded(original)')),  # original order
        (9, 'refunded2', _('order refunded(reverse)')),  # refund order
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Customer'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _('Booking order')
        verbose_name_plural = _('Booking orders')


class Booking(model_utils_models.TimeStampedModel):
    SEASON_CHOICES = Choices(
        (0, 'low', _('Low season')),
        (1, 'high', _('High season')),
    )

    DAY_CHOICES = Choices(
        (0, 'weekday', _('Weekday')),
        (1, 'weekend', _('Weekend')),
    )

    SLOT_CHOICES = Choices(
        (0, 'morning', _('Morning')),
        (1, 'daytime', _('Daytime')),
        (2, 'twilight', _('Twilight')),
        (3, 'night', _('Night')),
    )

    HOLE_CHOICES = Choices(
        (0, 'hole18', _('18 Holes')),
        (1, 'hole9', _('9 Holes')),
        (2, 'hole27', _('27 Holes')),
        (3, 'hole36', _('36 Holes')),
    )

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

    round_date = models.DateField(
        verbose_name=_('Round day'),
        db_index=True,
    )

    round_time = models.TimeField(
        verbose_name=_('Round time'),
    )

    pax = models.IntegerField(
        verbose_name=_('Pax'),
        default=4,
    )

    hole = models.IntegerField(
        verbose_name=_('No. of holes'),
        choices=HOLE_CHOICES,
        default=HOLE_CHOICES.hole18,
        db_index=True,
    )

    green_fee_sales = models.DecimalField(
        verbose_name=_('Green fee sales'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    cart_fee_sales = models.DecimalField(
        verbose_name=_('Cart fee sales'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    caddie_fee_sales = models.DecimalField(
        verbose_name=_('Caddie fee sales'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    green_fee_pay_on_arrival = models.BooleanField(
        verbose_name=_('Green fee pay on arrival'),
        default=False,
        db_index=True,
    )

    cart_fee_pay_on_arrival = models.BooleanField(
        verbose_name=_('Cart fee pay on arrival'),
        default=False,
        db_index=True,
    )

    caddie_fee_pay_on_arrival = models.BooleanField(
        verbose_name=_('Caddie fee pay on arrival'),
        default=False,
        db_index=True,
    )

    green_fee_cost = models.DecimalField(
        verbose_name=_('Green fee cost'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    cart_fee_cost = models.DecimalField(
        verbose_name=_('Cart fee cost'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    cart_fee_deducted_from_deposit = models.IntegerField(
        verbose_name=_('Cart fee deducted from deposit'),
        default=0,
    )

    caddie_fee_cost = models.DecimalField(
        verbose_name=_('Caddie fee cost'),
        max_digits=11,
        decimal_places=0,
        help_text=_('THB'),
    )

    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=255,
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=255,
    )

    memo = models.TextField(
        verbose_name=_('Memo'),
        blank=True,
        null=True,
    )

    season = models.IntegerField(
        verbose_name=_('High/Low Season'),
        choices=SEASON_CHOICES,
        default=SEASON_CHOICES.high,
        db_index=True,
    )

    day_of_week = models.IntegerField(
        verbose_name=_('Day of week'),
        choices=DAY_CHOICES,
        default=DAY_CHOICES.weekday,
        db_index=True,
    )

    slot = models.IntegerField(
        verbose_name=_('Time slot'),
        choices=SLOT_CHOICES,
        default=SLOT_CHOICES.morning,
        db_index=True,
    )

    stand_by = models.BooleanField(
        verbose_name=_('Stand-by'),
        default=False,
    )

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')


class Golfer(model_utils_models.TimeStampedModel):
    booking = models.ForeignKey(
        'windmill.Booking',
        verbose_name=_('Daily booking'),
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=255,
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('Golfer')
        verbose_name_plural = _('Golfers')


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
