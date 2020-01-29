from django.conf import settings

# Week day max
WEEKDAY_MAX = getattr(settings, 'WEEKDAY_MAX', 28)

# Weekend max
WEEKEND_MAX = getattr(settings, 'WEEKEND_MAX', 20)
