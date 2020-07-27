from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _('NA-ONE Communication')
admin.site.site_title = _('NA-ONE Communication')
admin.site.index_title = _('NA-ONE Communication')


class AssetTransactionInline(admin.TabularInline):
    model = models.NaoneAssetTransaction
    ordering = ['fee', 'cash_flow']
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
    list_display = (
    'day', 'time', 'agency', 'customer_name', 'pax', 'hole', 'booking_status', 'slot', 'type', 'tee_off_status')
    list_display_links = ('day', 'time', 'customer_name')
    list_filter = ('booking_status', 'tee_off_status', 'type', 'agency')
    inlines = [AssetTransactionInline, ]
    date_hierarchy = 'day'
    ordering = ['-day', '-time']
    readonly_fields = ('sales', 'profit')
    fieldsets = (
        (_('Booking info'), {
            'fields': (
                'agency', 'customer_name', 'phone', 'booking_status', 'sales', 'profit',
            )
        }),
        (_('Tee off info'), {
            'fields': (
                'pax', 'day', 'time',
                'season', 'day_of_week', 'slot',
                'hole', 'type', 'tee_off_status', 'remarks',
            )
        }),
    )

    class Media:
        js = ('admin/js/jquery.init.js', 'js/admin/windmill/teeoff.js')


class NaoneAssetAdmin(admin.ModelAdmin):
    list_display = ('asset_type', 'name', 'balance')
    list_filter = ('asset_type',)
    ordering = ('asset_type',)


class NaoneAssetTransaction(admin.ModelAdmin):
    list_display = ('fee', 'cash_flow', 'input_type', 'asset', 'unit_price', 'amount', 'transaction_date')
    list_filter = ('fee', 'cash_flow', 'input_type', 'asset')
    date_hierarchy = 'transaction_date'
    ordering = ['-transaction_date', 'fee', 'cash_flow']


admin.site.register(models.Agency, AgencyAdmin)
admin.site.register(models.TeeOffTime, TeeOffTimeAdmin)
admin.site.register(models.NaoneAsset, NaoneAssetAdmin)
admin.site.register(models.NaoneAssetTransaction, NaoneAssetTransaction)
