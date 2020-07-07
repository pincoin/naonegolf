import calendar

from django import template
from django.utils import timezone
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter
def month_name(month_number):
    return _(calendar.month_name[int(month_number)])

