from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class Agency(model_utils_models.TimeStampedModel):
    ENTITY_TYPE = Choices(
        (0, 'naone', _('NA-ONE')),
        (1, 'swgc', _('SWGC')),
        (2, 'member', _('SWGC Member')),
        (3, 'company', _('Company')),
    )

    TYPE_CHOICES = Choices(
        (0, 'normal', _('Normal')),
        (1, 'prepaid', _('Prepaid')),
    )

    entity = models.IntegerField(
        verbose_name=_('Agency entity type'),
        choices=ENTITY_TYPE,
        default=ENTITY_TYPE.company,
        db_index=True,
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
        return '{} [{}/{}]'.format(self.name, self.get_entity_display(), self.get_type_display())


class TeeOffTime(model_utils_models.TimeStampedModel):
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

    TYPE_CHOICES = Choices(
        (0, 'fixed', _('Fixed')),
        (1, 'stand_by', _('Stand-by'))
    )

    TEE_OFF_STATUS_CHOICES = Choices(
        (0, 'open', _('Open')),
        (1, 'held', _('Held')),
        (2, 'sold', _('Sold')),
        (3, 'revoked', _('Revoked')),
    )

    HOLE_CHOICES = Choices(
        (0, 'hole18', _('18 Holes')),
        (1, 'hole9', _('9 Holes')),
        (2, 'hole27', _('27 Holes')),
        (3, 'hole36', _('36 Holes')),
    )

    BOOKING_STATUS_CHOICES = Choices(
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

    booking_status = models.IntegerField(
        verbose_name=_('Booking status'),
        choices=BOOKING_STATUS_CHOICES,
        default=BOOKING_STATUS_CHOICES.order_opened,
        db_index=True,
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

    type = models.IntegerField(
        verbose_name=_('Tee off type'),
        choices=TYPE_CHOICES,
        default=TYPE_CHOICES.fixed,
        db_index=True,
    )

    tee_off_status = models.IntegerField(
        verbose_name=_('Tee off status'),
        choices=TEE_OFF_STATUS_CHOICES,
        default=TEE_OFF_STATUS_CHOICES.open,
        db_index=True,
    )

    day = models.DateField(
        verbose_name=_('Round day'),
        db_index=True,
    )

    time = models.TimeField(
        verbose_name=_('Tee-off time'),
    )

    class Meta:
        verbose_name = _('Tee-off time')
        verbose_name_plural = _('Tee-off times')

    def __str__(self):
        return '{} {}'.format(self.day, self.time)


class NaoneAsset(model_utils_models.TimeStampedModel):
    ASSET_TYPE_CHOICES = Choices(
        (0, 'petty_cash', _('Petty cash')),
        (1, 'prepaid', _('Prepaid')),
        (2, 'bank_account', _('Bank account')),
        (3, 'ecoupon', _('E-Coupon')),
    )

    asset_type = models.IntegerField(
        verbose_name=_('Asset type'),
        choices=ASSET_TYPE_CHOICES,
        default=ASSET_TYPE_CHOICES.petty_cash,
        db_index=True,
    )

    name = models.CharField(
        verbose_name=_('Asset name'),
        max_length=255,
    )

    balance = models.DecimalField(
        verbose_name=_('Asset balance'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    class Meta:
        verbose_name = _('NA-ONE Asset')
        verbose_name_plural = _('NA-ONE Assets')

    def __str__(self):
        return '{} {}'.format(self.name, self.balance)


class NaoneAssetTransaction(model_utils_models.TimeStampedModel):
    FEE_CHOICES = Choices(
        (0, 'green_fee', _('Green fee')),
        (1, 'caddie_fee', _('Caddie fee')),
        (2, 'cart_fee', _('Cart fee')),
    )

    CASH_FLOW_CHOICES = Choices(
        (0, 'cash_in', _('Cash-in')),
        (1, 'cash_out', _('Cash-out')),
    )

    INPUT_TYPE_CHOICES = Choices(
        (0, 'manual', _('Manual input')),
        (1, 'closing', _('Closing input')),
    )

    order = models.ForeignKey(
        'windmill.TeeOffTime',
        verbose_name=_('Tee-off'),
        db_index=True,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    fee = models.IntegerField(
        verbose_name=_('Fee'),
        choices=FEE_CHOICES,
        default=FEE_CHOICES.green_fee,
        db_index=True,
    )

    cash_flow = models.IntegerField(
        verbose_name=_('Cash flow'),
        choices=CASH_FLOW_CHOICES,
        default=CASH_FLOW_CHOICES.cash_in,
        db_index=True,
    )

    input_type = models.IntegerField(
        verbose_name=_('Input type'),
        choices=INPUT_TYPE_CHOICES,
        default=INPUT_TYPE_CHOICES.manual,
        db_index=True,
    )

    asset = models.ForeignKey(
        'windmill.NaoneAsset',
        verbose_name=_('Asset'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    unit_price = models.DecimalField(
        verbose_name=_('Unit price'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    amount = models.DecimalField(
        verbose_name=_('Amount'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    transaction_date = models.DateTimeField(
        verbose_name=_('Transaction date'),
    )

    remarks = models.TextField(
        verbose_name=_('Remarks'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Asset transaction')
        verbose_name_plural = _('Asset transactions')

    def __str__(self):
        return 'asset transaction - {} {}'.format(self.amount, self.transaction_date)


class NaoneManagingBook(model_utils_models.TimeStampedModel):
    ASSET_TYPE_CHOICES = Choices(
        (0, 'petty_cash', _('Petty cash')),
        (1, 'prepaid', _('Prepaid')),
        (2, 'ecoupon', _('E-Coupon')),
    )

    CASH_FLOW_CHOICES = Choices(
        (0, 'cash_in', _('Cash-in')),
        (1, 'cash_out', _('Cash-out')),
    )

    INPUT_TYPE_CHOICES = Choices(
        (0, 'manual', _('Manual input')),
        (1, 'closing', _('Closing input')),
    )

    date = models.DateField(
        verbose_name=_('Transaction date'),
        db_index=True,
    )

    agency = models.ForeignKey(
        'windmill.Agency',
        verbose_name=_('Agency'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    memo = models.CharField(
        verbose_name=_('Transaction memo'),
        max_length=255,
    )

    asset_type = models.IntegerField(
        verbose_name=_('Asset type'),
        choices=ASSET_TYPE_CHOICES,
        default=ASSET_TYPE_CHOICES.petty_cash,
        db_index=True,
    )

    cash_flow = models.IntegerField(
        verbose_name=_('Cash flow'),
        choices=CASH_FLOW_CHOICES,
        default=CASH_FLOW_CHOICES.cash_in,
        db_index=True,
    )

    count = models.IntegerField(
        verbose_name=_('Count'),
        default=0,
    )

    amount = models.DecimalField(
        verbose_name=_('Amount'),
        max_digits=11,
        decimal_places=0,
        default=Decimal('0'),
        help_text=_('THB'),
    )

    input_type = models.IntegerField(
        verbose_name=_('Input type'),
        choices=INPUT_TYPE_CHOICES,
        default=INPUT_TYPE_CHOICES.manual,
        db_index=True,
    )

    class Meta:
        verbose_name = _('NA-ONE Managing Book')
        verbose_name_plural = _('NA-ONE Managing Book')

    def __str__(self):
        return '{} {} {}'.format(self.agency, self.get_cash_flow_display(), self.amount)
