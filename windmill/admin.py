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


class DailyBookingAdmin(admin.ModelAdmin):
    list_display = ('day',)
    inlines = [TeeOffTimeInline, ]
    ordering = ('day',)
    date_hierarchy = 'day'


admin.site.register(models.DailyBooking, DailyBookingAdmin)
