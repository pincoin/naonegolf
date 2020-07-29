import calendar

from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter
def month_name(month_number):
    return _(calendar.month_name[int(month_number)])


@register.filter
def asset_name(name):
    if name == 'Petty cash':
        return '시재'
    elif name == '[Account] SCB':
        return '통장'
    elif name == 'E-Card':
        return 'E카드'
    elif name == '[Deposit] TOTO':
        return '선납'
    else:
        return name
