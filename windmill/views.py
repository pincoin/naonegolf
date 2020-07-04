from django.db.models import (
    Sum, Q
)
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
        return models.TeeOffTime.objects \
            .select_related('agency') \
            .prefetch_related('naoneassettransaction_set__asset') \
            .filter(day__year=self.kwargs['year'],
                    day__month=self.kwargs['month'],
                    day__day=self.kwargs['day']) \
            .annotate(total_petty_cash_in=Sum('naoneassettransaction__amount',
                                              filter=Q(naoneassettransaction__cash_flow
                                                       =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in,
                                                       naoneassettransaction__asset__asset_type
                                                       =models.NaoneAsset.ASSET_TYPE_CHOICES.petty_cash),
                                              ),
                      total_petty_cash_out=Sum('naoneassettransaction__amount',
                                               filter=Q(naoneassettransaction__cash_flow
                                                        =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out,
                                                        naoneassettransaction__asset__asset_type
                                                        =models.NaoneAsset.ASSET_TYPE_CHOICES.petty_cash),
                                               ),
                      )
