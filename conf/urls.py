from django.contrib import admin
from django.urls import (
    path, include
)

from .views import HomeView

urlpatterns = [
    path('',
         HomeView.as_view(), name='home'),

    path('accounts/',
         include('member.urls')),

    path('admin/',
         admin.site.urls),
]
