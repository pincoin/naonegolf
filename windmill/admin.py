from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _('NA-ONE Communication')
admin.site.site_title = _('NA-ONE Communication')
admin.site.index_title = _('NA-ONE Communication')


class TeeOffTimeInline(admin.TabularInline):
    model = models.TeeOffTime
    extra = 0
    fields = ('time', 'slot', 'type', 'status')
    ordering = ['time', ]


class RoundDayAdmin(admin.ModelAdmin):
    list_display = ('day', 'season', 'day_of_week', 'pax', 'sales', 'cost', 'cart_fee_deducted_from_deposit')
    inlines = [TeeOffTimeInline, ]
    ordering = ('-day',)
    date_hierarchy = 'day'


class TeeOffTimeAdmin(admin.ModelAdmin):
    list_display = ('day', 'time', 'slot', 'type', 'status')
    list_display_links = ('day', 'time')
    list_filter = ('status', 'type')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'pax', 'hole', 'status')
    list_filter = ('status', 'hole')
    filter_horizontal = ['tee_off', ]

    fieldsets = (
        (_('Booking info'), {
            'fields': (
                'customer_name', 'tee_off', 'pax', 'hole', 'status',
            )
        }),
        (_('Payment info'), {
            'fields': (
                ('green_fee_pay_on_arrival', 'green_fee_sales', 'green_fee_cost'),
                ('caddie_fee_pay_on_arrival', 'caddie_fee_sales', 'caddie_fee_cost'),
                ('cart_fee_pay_on_arrival', 'cart_fee_sales', 'cart_fee_deducted_from_deposit', 'cart_fee_cost',),
            )
        }),
    )


admin.site.register(models.RoundDay, RoundDayAdmin)
admin.site.register(models.TeeOffTime, TeeOffTimeAdmin)
admin.site.register(models.Booking, BookingAdmin)
