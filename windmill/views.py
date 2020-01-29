from django.utils import timezone
from django.views import generic

from . import models


class TeeOffListView(generic.ListView):
    context_object_name = 'days'

    template_name = 'windmill/tee_off_list.html'

    def get_queryset(self):
        queryset = models.DailyBooking.objects \
            .prefetch_related('teeofftime_set') \
            .filter(day__gte=timezone.make_aware(timezone.localtime().today())) \
            .order_by('day')

        return queryset
