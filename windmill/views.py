from django.views import generic

from . import models


class TeeOffListView(generic.TemplateView):
    context_object_name = 'days'

    template_name = 'windmill/tee_off_list.html'


class BookingCreateForm(generic.TemplateView):
    template_name = 'windmill/booking_create.html'


class DailyStatusReport(generic.ListView):
    context_object_name = 'tee_off_times'
    template_name = 'windmill/daily_status_report.html'

    def get_queryset(self):
        return models.TeeOffTime.objects.filter(day__year=self.kwargs['year'],
                                                day__month=self.kwargs['month'],
                                                day__day=self.kwargs['day'])
