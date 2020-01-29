from django.urls import path

from . import views

app_name = 'golf'

urlpatterns = [
    path('holiday-list/',
         views.HolidayListView.as_view(), name='holiday-list'),
]
