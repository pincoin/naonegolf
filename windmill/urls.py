from django.urls import path

from . import views

app_name = 'windmill'

urlpatterns = [
    path('tee-off-list/',
         views.TeeOffListView.as_view(), name='tee-off-list'),
]
