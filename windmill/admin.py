from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _('NA-ONE Communication')
admin.site.site_title = _('NA-ONE Communication')
admin.site.index_title = _('NA-ONE Communication')


class DailyBookingAdmin(admin.ModelAdmin):
    list_display = ('day',)
    ordering = ('day',)
    date_hierarchy = 'day'


admin.site.register(models.DailyBooking, DailyBookingAdmin)
