from django.utils import timezone
from django.views import generic

from . import models


class HolidayListView(generic.ListView):
    context_object_name = 'holidays'

    template_name = 'golf/holiday_list.html'

    def get_queryset(self):
        queryset = models.Holiday.objects \
            .filter(holiday__gte=timezone.make_aware(timezone.localtime().today()),
                    country=models.Holiday.COUNTRY_CHOICES.thailand)

        print(queryset)

        return queryset.order_by('holiday')
