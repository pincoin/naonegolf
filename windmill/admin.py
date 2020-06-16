from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _('NA-ONE Communication')
admin.site.site_title = _('NA-ONE Communication')
admin.site.index_title = _('NA-ONE Communication')


class AssetTransactionInline(admin.TabularInline):
    model = models.NaoneAssetTransaction
    ordering = ['-transaction_date', ]
    extra = 1


class TeeOffTimeInline(admin.StackedInline):
    model = models.TeeOffTime
    extra = 0
    ordering = ['time', ]


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'type',
                    'weekday_day', 'weekend_morning', 'weekend_afternoon', 'twilight', 'night')
    list_filter = ('entity', 'type')


class TeeOffTimeAdmin(admin.ModelAdmin):
    list_display = ('day', 'time', 'slot', 'type', 'tee_off_status')
    list_display_links = ('day', 'time')
    list_filter = ('tee_off_status', 'type')
    inlines = [AssetTransactionInline, ]
    fieldsets = (
        (_('Booking info'), {
            'fields': (
                'agency', 'customer_name', 'booking_status',
            )
        }),
        (_('Tee off info'), {
            'fields': (
                'pax', 'day', 'time',
                'season', 'day_of_week', 'slot',
                'hole', 'type', 'tee_off_status',
            )
        }),
    )


class NaoneAssetAdmin(admin.ModelAdmin):
    list_display = ('asset_type', 'name', 'balance')
    list_filter = ('asset_type',)


class NaoneManagingBookAdmin(admin.ModelAdmin):
    list_display = ('date', 'memo', 'agency', 'asset_type', 'cash_flow', 'count', 'amount_comma_separated')
    list_display_links = ('date', 'memo', 'agency')
    list_filter = ('agency', 'asset_type', 'cash_flow')
    ordering = ['-date', ]

    def amount_comma_separated(self, instance):
        return '{:,}'.format(instance.amount)

    amount_comma_separated.short_description = _('Amount')


admin.site.register(models.Agency, AgencyAdmin)
admin.site.register(models.TeeOffTime, TeeOffTimeAdmin)
admin.site.register(models.NaoneAsset, NaoneAssetAdmin)
admin.site.register(models.NaoneManagingBook, NaoneManagingBookAdmin)
