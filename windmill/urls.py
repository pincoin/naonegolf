from django.urls import (
    path, re_path
)

from . import views

app_name = 'windmill'

urlpatterns = [
    path('tee-off-list/',
         views.TeeOffListView.as_view(), name='tee-off-list'),

    path('booking/add/',
         views.BookingCreateForm.as_view(), name='booking-create'),

    path('reports/',
         views.Report.as_view(), name='status-report'),

    re_path(r'^reports/(?P<year>[0-9]{4})/$',
            views.YearlyStatusReport.as_view(), name='yearly-status-report'),

    re_path(r'^reports/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
            views.MonthlyStatusReport.as_view(), name='monthly-status-report'),

    re_path(r'^reports/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
            views.DailyStatusReport.as_view(), name='daily-status-report'),
]
