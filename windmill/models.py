from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class Agency(model_utils_models.TimeStampedModel):
    TYPE_CHOICES = Choices(
        (0, 'normal', _('Normal')),
        (1, 'prepaid', _('Prepaid')),
    )

    type = models.IntegerField(
        verbose_name=_('Pay type'),
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES.normal,
        db_index=True,
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
    )

    weekday_day = models.DecimalField(
        verbose_name=_('Weekday day'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    weekend_morning = models.DecimalField(
        verbose_name=_('Weekend morning'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    weekend_afternoon = models.DecimalField(
        verbose_name=_('Weekend afternoon'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    twilight = models.DecimalField(
        verbose_name=_('Twilight'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    night = models.DecimalField(
        verbose_name=_('Night'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')

    def __str__(self):
        return '{} {}'.format(self.name, self.type)


class RoundDay(model_utils_models.TimeStampedModel):
    SEASON_CHOICES = Choices(
        (0, 'low', _('Low season')),
        (1, 'high', _('High season')),
    )

    DAY_CHOICES = Choices(
        (0, 'weekday', _('Weekday')),
        (1, 'weekend', _('Weekend')),
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

    day = models.DateField(
        verbose_name=_('Booking Day'),
        db_index=True,
        unique=True,
    )

    pax = models.IntegerField(
        verbose_name=_('Pax'),
        default=0,
    )

    sales = models.DecimalField(
        verbose_name=_('Daily sales'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    cost = models.DecimalField(
        verbose_name=_('Daily cost'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    cart_fee_deducted_from_deposit = models.IntegerField(
        verbose_name=_('Cart fee deducted from deposit'),
        default=0,
    )

    class Meta:
        verbose_name = _('Round day')
        verbose_name_plural = _('Round days')

    def __str__(self):
        return '{}'.format(self.day)


class TeeOffTime(model_utils_models.TimeStampedModel):
    SLOT_CHOICES = Choices(
        (0, 'morning', _('Morning')),
        (1, 'daytime', _('Daytime')),
        (2, 'twilight', _('Twilight')),
        (3, 'night', _('Night')),
    )

    TYPE_CHOICES = Choices(
        (0, 'fixed', _('Fixed')),
        (1, 'stand_by', _('Stand-by'))
    )

    STATUS_CHOICES = Choices(
        (0, 'open', _('Open')),
        (1, 'held', _('Held')),
        (2, 'sold', _('Sold')),
        (3, 'revoked', _('Revoked')),
    )

    slot = models.IntegerField(
        verbose_name=_('Time slot'),
        choices=SLOT_CHOICES,
        default=SLOT_CHOICES.morning,
        db_index=True,
    )

    type = models.IntegerField(
        verbose_name=_('Type'),
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES.fixed,
        db_index=True,
    )

    status = models.IntegerField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.open,
        db_index=True,
    )

    day = models.ForeignKey(
        'windmill.RoundDay',
        verbose_name=_('Round day'),
        on_delete=models.CASCADE,
    )

    booking = models.ForeignKey(
        'windmill.Booking',
        verbose_name=_('Booking'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    time = models.TimeField(
        verbose_name=_('Tee-off time'),
    )

    class Meta:
        verbose_name = _('Tee-off time')
        verbose_name_plural = _('Tee-off times')

    def __str__(self):
        return '{} {}'.format(self.day, self.time)


class Booking(model_utils_models.TimeStampedModel):
    HOLE_CHOICES = Choices(
        (0, 'hole18', _('18 Holes')),
        (1, 'hole9', _('9 Holes')),
        (2, 'hole27', _('27 Holes')),
        (3, 'hole36', _('36 Holes')),
    )

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

    agency = models.ForeignKey(
        'windmill.Agency',
        verbose_name=_('Agency'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    customer_name = models.CharField(
        verbose_name=_('Customer name'),
        max_length=255,
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

    status = models.IntegerField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.order_opened,
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

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def __str__(self):
        return '{}'.format(self.customer_name)
