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

    total_sales = 0
    total_cost = 0
    total_profit = 0

    def get_queryset(self):
        qs = models.TeeOffTime.objects \
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
                      total_sales=Sum('naoneassettransaction__amount',
                                      filter=Q(naoneassettransaction__cash_flow
                                               =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in),
                                      ),
                      total_cost=Sum('naoneassettransaction__amount',
                                     filter=Q(naoneassettransaction__cash_flow
                                              =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out),
                                     ),
                      )

        for teeoff in qs:
            for transaction in teeoff.naoneassettransaction_set.all():
                if transaction.cash_flow == models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in:
                    self.total_sales += transaction.amount
                elif transaction.cash_flow == models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out:
                    self.total_cost += transaction.amount

        return qs

    def get_context_data(self, **kwargs):
        context = super(DailyStatusReport, self).get_context_data(**kwargs)

        context['total_sales'] = self.total_sales
        context['total_cost'] = self.total_cost
        context['total_profit'] = self.total_sales - self.total_cost

        return context
