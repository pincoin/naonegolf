from django import template

from django.utils import timezone

register = template.Library()


@register.simple_tag
def get_date(year, month, day):
    return timezone.datetime(int(year), int(month), int(day)).strftime('%Y-%m-%d %a')
