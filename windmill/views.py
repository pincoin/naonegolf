import calendar

from django.db.models import (
    Sum, Q, Count
)
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.views import generic

from . import models


class TeeOffListView(generic.TemplateView):
    context_object_name = 'days'

    template_name = 'windmill/tee_off_list.html'


class BookingCreateForm(generic.TemplateView):
    template_name = 'windmill/booking_create.html'


class Report(generic.TemplateView):
    context_object_name = 'reports'

    template_name = 'windmill/report.html'

    def get_context_data(self, **kwargs):
        context = super(Report, self).get_context_data(**kwargs)

        context['years'] = list(range((timezone.datetime.now() + timezone.timedelta(days=90)).year, 2019, -1))

        return context


class YearlyStatusReport(generic.TemplateView):
    template_name = 'windmill/yearly_status_report.html'

    def get_context_data(self, **kwargs):
        context = super(YearlyStatusReport, self).get_context_data(**kwargs)

        if int(self.kwargs['year']) == timezone.datetime.now().year:
            month = timezone.datetime.now().month + 3

            if month > 12:
                month = 12

            context['months'] = list(range(month, 0, -1))
            context['this_year'] = True
            context['this_month'] = timezone.datetime.now().month

        elif int(self.kwargs['year']) <= timezone.datetime.now().year:
            context['months'] = list(range(1, 13))
        else:
            context['months'] = list(range(1, 4))

        context['year'] = self.kwargs['year']

        return context


class MonthlyStatusReport(generic.TemplateView):
    template_name = 'windmill/monthly_status_report.html'

    def get_context_data(self, **kwargs):
        context = super(MonthlyStatusReport, self).get_context_data(**kwargs)

        qs = models.TeeOffTime.objects \
            .filter(day__year=int(self.kwargs['year']), day__month=int(self.kwargs['month'])) \
            .annotate(day1=TruncDay('day')) \
            .values('day1') \
            .annotate(count=Count('id')) \
            .values('day1', 'count') \
            .order_by('-day1')

        context['days'] = []

        for i in list(range(1, calendar.monthrange(int(self.kwargs['year']), int(self.kwargs['month']))[1] + 1)):
            found = False
            for s in qs:
                if str(s['day1']) == timezone.datetime(int(self.kwargs['year']),
                                                       int(self.kwargs['month']),
                                                       int(i)).strftime('%Y-%m-%d'):
                    found = True
                    context['days'].append({'day': i, 'count': s['count']})
                    break

            if not found:
                context['days'].append({'day': i, 'count': 0})

        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']

        return context


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

        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']

        return context


class MonthlyDailyStatusReport(generic.ListView):
    context_object_name = 'tee_off_times'
    template_name = 'windmill/monthly_daily_status_report.html'

    total_sales = 0
    total_cost = 0
    total_profit = 0

    def get_queryset(self):
        qs = models.TeeOffTime.objects \
            .select_related('agency') \
            .prefetch_related('naoneassettransaction_set__asset') \
            .filter(day__year=self.kwargs['year'],
                    day__month=self.kwargs['month']) \
            .annotate(green_fee_price=Sum('naoneassettransaction__unit_price',
                                          filter=Q(naoneassettransaction__fee
                                                   =models.NaoneAssetTransaction.FEE_CHOICES.green_fee,
                                                   naoneassettransaction__cash_flow
                                                   =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in)),
                      green_fee_subtotal=Sum('naoneassettransaction__amount',
                                             filter=Q(naoneassettransaction__fee
                                                      =models.NaoneAssetTransaction.FEE_CHOICES.green_fee,
                                                      naoneassettransaction__cash_flow
                                                      =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in)),

                      green_fee_cost=Sum('naoneassettransaction__unit_price',
                                         filter=Q(naoneassettransaction__fee
                                                  =models.NaoneAssetTransaction.FEE_CHOICES.green_fee,
                                                  naoneassettransaction__cash_flow
                                                  =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out)),
                      green_fee_cost_subtotal=Sum('naoneassettransaction__amount',
                                                  filter=Q(naoneassettransaction__fee
                                                           =models.NaoneAssetTransaction.FEE_CHOICES.green_fee,
                                                           naoneassettransaction__cash_flow
                                                           =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out)),
                      caddie_fee_price=Sum('naoneassettransaction__unit_price',
                                           filter=Q(naoneassettransaction__fee
                                                    =models.NaoneAssetTransaction.FEE_CHOICES.caddie_fee,
                                                    naoneassettransaction__cash_flow
                                                    =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in)),
                      caddie_fee_subtotal=Sum('naoneassettransaction__amount',
                                              filter=Q(naoneassettransaction__fee
                                                       =models.NaoneAssetTransaction.FEE_CHOICES.caddie_fee,
                                                       naoneassettransaction__cash_flow
                                                       =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in)),
                      caddie_fee_cost=Sum('naoneassettransaction__unit_price',
                                          filter=Q(naoneassettransaction__fee
                                                   =models.NaoneAssetTransaction.FEE_CHOICES.caddie_fee,
                                                   naoneassettransaction__cash_flow
                                                   =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out)),
                      caddie_fee_cost_subtotal=Sum('naoneassettransaction__amount',
                                                   filter=Q(naoneassettransaction__fee
                                                            =models.NaoneAssetTransaction.FEE_CHOICES.caddie_fee,
                                                            naoneassettransaction__cash_flow
                                                            =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out)),
                      cart_fee_price=Sum('naoneassettransaction__unit_price',
                                         filter=Q(naoneassettransaction__fee
                                                  =models.NaoneAssetTransaction.FEE_CHOICES.cart_fee,
                                                  naoneassettransaction__cash_flow
                                                  =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in)),
                      cart_fee_subtotal=Sum('naoneassettransaction__amount',
                                            filter=Q(naoneassettransaction__fee
                                                     =models.NaoneAssetTransaction.FEE_CHOICES.cart_fee,
                                                     naoneassettransaction__cash_flow
                                                     =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in)),
                      cart_fee_cost=Sum('naoneassettransaction__unit_price',
                                        filter=Q(naoneassettransaction__fee
                                                 =models.NaoneAssetTransaction.FEE_CHOICES.cart_fee,
                                                 naoneassettransaction__cash_flow
                                                 =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out)),
                      cart_fee_cost_subtotal=Sum('naoneassettransaction__amount',
                                                 filter=Q(naoneassettransaction__fee
                                                          =models.NaoneAssetTransaction.FEE_CHOICES.cart_fee,
                                                          naoneassettransaction__cash_flow
                                                          =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out)),
                      total_petty_cash_in=Sum('naoneassettransaction__amount',
                                              filter=Q(naoneassettransaction__cash_flow
                                                       =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in,
                                                       naoneassettransaction__asset__asset_type
                                                       =models.NaoneAsset.ASSET_TYPE_CHOICES.petty_cash)),
                      total_petty_cash_out=Sum('naoneassettransaction__amount',
                                               filter=Q(naoneassettransaction__cash_flow
                                                        =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out,
                                                        naoneassettransaction__asset__asset_type
                                                        =models.NaoneAsset.ASSET_TYPE_CHOICES.petty_cash)),
                      total_bank_in=Sum('naoneassettransaction__amount',
                                        filter=Q(naoneassettransaction__cash_flow
                                                 =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in,
                                                 naoneassettransaction__asset__asset_type
                                                 =models.NaoneAsset.ASSET_TYPE_CHOICES.bank_account)),
                      total_bank_out=Sum('naoneassettransaction__amount',
                                         filter=Q(naoneassettransaction__cash_flow
                                                  =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out,
                                                  naoneassettransaction__asset__asset_type
                                                  =models.NaoneAsset.ASSET_TYPE_CHOICES.bank_account)),
                      total_prepaid_in=Sum('naoneassettransaction__amount',
                                           filter=Q(naoneassettransaction__cash_flow
                                                    =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in,
                                                    naoneassettransaction__asset__asset_type
                                                    =models.NaoneAsset.ASSET_TYPE_CHOICES.prepaid)),
                      total_prepaid_out=Sum('naoneassettransaction__amount',
                                            filter=Q(naoneassettransaction__cash_flow
                                                     =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out,
                                                     naoneassettransaction__asset__asset_type
                                                     =models.NaoneAsset.ASSET_TYPE_CHOICES.prepaid)),
                      total_sales=Sum('naoneassettransaction__amount',
                                      filter=Q(naoneassettransaction__cash_flow
                                               =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in),
                                      ),
                      total_cost=Sum('naoneassettransaction__amount',
                                     filter=Q(naoneassettransaction__cash_flow
                                              =models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out),
                                     ),
                      ) \
            .order_by('day', 'time')

        for teeoff in qs:
            teeoff.total_petty_cash_balance = teeoff.total_petty_cash_in or 0 - teeoff.total_petty_cash_out or 0
            teeoff.total_bank_balance = teeoff.total_bank_in or 0 - teeoff.total_bank_out or 0
            # teeoff.total_prepaid_balance = teeoff.total_prepaid_in or 0 - teeoff.total_prepaid_out or 0

            for t in teeoff.naoneassettransaction_set.all():
                if t.cash_flow == models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in:
                    if t.fee == models.NaoneAssetTransaction.FEE_CHOICES.green_fee:
                        teeoff.green_fee_asset = t.asset.name
                    elif t.fee == models.NaoneAssetTransaction.FEE_CHOICES.caddie_fee:
                        teeoff.caddie_fee_asset = t.asset.name
                    elif t.fee == models.NaoneAssetTransaction.FEE_CHOICES.cart_fee:
                        teeoff.cart_fee_asset = t.asset.name
                else:
                    if t.fee == models.NaoneAssetTransaction.FEE_CHOICES.green_fee:
                        teeoff.green_fee_cost_asset = t.asset.name
                    elif t.fee == models.NaoneAssetTransaction.FEE_CHOICES.caddie_fee:
                        teeoff.caddie_fee_cost_asset = t.asset.name
                    elif t.fee == models.NaoneAssetTransaction.FEE_CHOICES.cart_fee:
                        teeoff.cart_fee_cost_asset = t.asset.name
                        teeoff.ecard = t.amount / t.unit_price if teeoff.cart_fee_cost_asset == 'E-Card' else 0

        for teeoff in qs:
            for transaction in teeoff.naoneassettransaction_set.all():
                if transaction.cash_flow == models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_in:
                    self.total_sales += transaction.amount
                elif transaction.cash_flow == models.NaoneAssetTransaction.CASH_FLOW_CHOICES.cash_out:
                    self.total_cost += transaction.amount

        return qs

    def get_context_data(self, **kwargs):
        context = super(MonthlyDailyStatusReport, self).get_context_data(**kwargs)

        context['total_sales'] = self.total_sales
        context['total_cost'] = self.total_cost
        context['total_profit'] = self.total_sales - self.total_cost

        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']

        return context
