from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class Holiday(model_utils_models.TimeStampedModel):
    COUNTRY_CHOICES = Choices(
        (1, 'thailand', _('Thailand')),
        (2, 'south_korea', _('South Korea')),
        (3, 'japan', _('Japan')),
        (4, 'china', _('China')),
    )

    title = models.CharField(
        verbose_name=_('Holiday name'),
        max_length=255,
    )

    holiday = models.DateField(
        verbose_name=_('Holiday day'),
        db_index=True,
    )

    country = models.IntegerField(
        verbose_name=_('Country code'),
        choices=COUNTRY_CHOICES,
        default=COUNTRY_CHOICES.thailand,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Holiday')
        verbose_name_plural = _('Holidays')

        unique_together = ('holiday', 'country')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.holiday, self.country)


class ClubProduct(model_utils_models.TimeStampedModel):
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

    class Meta:
        verbose_name = _('Golf club product')
        verbose_name_plural = _('Golf club products')

        unique_together = ('season', 'day_of_week', 'slot')

    def __str__(self):
        return '{} / {} / {}'.format(
            self.SEASON_CHOICES[self.season],
            self.DAY_CHOICES[self.day_of_week],
            self.SLOT_CHOICES[self.slot],
        )


class Club(model_utils_models.TimeStampedModel):
    HOLE_CHOICES = Choices(
        (0, 'eighteen', _('18 Holes')),
        (1, 'nine', _('9 Holes')),
        (2, 'twentyseven', _('27 Holes')),
        (3, 'thirtysix', _('36 Holes')),
    )

    COUNTRY_CHOICES = Choices(
        (1, 'thailand', _('Thailand')),
        (2, 'south_korea', _('South Korea')),
        (3, 'japan', _('Japan')),
        (4, 'china', _('China')),
    )

    title = models.CharField(
        verbose_name=_('Golf club name'),
        max_length=255,
    )

    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        blank=True,
        null=True,
    )

    website = models.URLField(
        verbose_name=_('Website'),
        max_length=255,
        blank=True,
        null=True,
    )

    hole = models.IntegerField(
        verbose_name=_('No. of holes'),
        choices=HOLE_CHOICES,
        default=HOLE_CHOICES.eighteen,
        db_index=True,
    )

    cart_rental_required = models.BooleanField(
        verbose_name=_('Cart rental required'),
        default=False,
        db_index=True,
    )

    cart_fee = models.DecimalField(
        verbose_name=_('Cart fee'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    caddie_fee = models.DecimalField(
        verbose_name=_('Caddie fee'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    high_season = models.IntegerField(
        verbose_name=_('High season'),
        default=0x0C03,  # b'110000000011'
    )

    max_high_weekday = models.PositiveIntegerField(
        verbose_name=_('Max # of High/Weekday'),
        default=0,
    )

    max_high_weekend = models.PositiveIntegerField(
        verbose_name=_('Max # of High/Weekend'),
        default=0,
    )

    max_low_weekday = models.PositiveIntegerField(
        verbose_name=_('Max # of Low/Weekday'),
        default=0,
    )

    max_low_weekend = models.PositiveIntegerField(
        verbose_name=_('Max # of Low/Weekend'),
        default=0,
    )

    country = models.IntegerField(
        verbose_name=_('Country code'),
        choices=COUNTRY_CHOICES,
        default=COUNTRY_CHOICES.thailand,
        db_index=True,
    )

    products = models.ManyToManyField(
        'golf.ClubProduct',
        through='golf.ClubProductListMembership'
    )

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.email, self.phone)


class ClubProductListMembership(models.Model):
    club = models.ForeignKey(
        'golf.Club',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    product_list = models.ForeignKey(
        'golf.ClubProduct',
        verbose_name=_('Product list'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    start_time = models.TimeField(
        verbose_name=_('Start time'),
    )

    end_time = models.TimeField(
        verbose_name=_('End time'),
    )

    list_price = models.DecimalField(
        verbose_name=_('List price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
    )

    class Meta:
        verbose_name = _('Product list membership')
        verbose_name_plural = _('Product list membership')

        unique_together = ('club', 'product_list')

    def __str__(self):
        return '{} - {}'.format(self.club.title, self.product_list)
