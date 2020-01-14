from importlib import import_module

from allauth.socialaccount import providers
from django.urls import (
    path
)

from . import views

app_name = 'member'

urlpatterns = [
    # Account
    path('login/',
         views.MemberLoginView.as_view(), name="account_login"),
    path('logout/',
         views.MemberLogoutView.as_view(), name="account_logout"),
]

# URL patterns for Line custom social providers
# Line provider requires PyJWT
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue

    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)

    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
