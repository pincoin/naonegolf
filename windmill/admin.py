from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _('NA-ONE Communication')
admin.site.site_title = _('NA-ONE Communication')
admin.site.index_title = _('NA-ONE Communication')


class TeeOffTimeInline(admin.TabularInline):
    model = models.TeeOffTime
    extra = 0
    fields = ('hour', 'minute', 'status')
    ordering = ['hour', 'minute']


class GolferInline(admin.TabularInline):
    model = models.Golfer
    extra = 0


class BookingOrderAdmin(admin.ModelAdmin):
    pass


class BookingAdmin(admin.ModelAdmin):
    inlines = [GolferInline, ]


class DailyBookingAdmin(admin.ModelAdmin):
    list_display = ('day',)
    inlines = [TeeOffTimeInline, ]
    ordering = ('day',)
    date_hierarchy = 'day'


admin.site.register(models.BookingOrder, BookingOrderAdmin)
admin.site.register(models.Booking, BookingAdmin)
admin.site.register(models.DailyBooking, DailyBookingAdmin)
