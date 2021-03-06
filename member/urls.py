from importlib import import_module

from allauth.socialaccount import providers
from django.urls import (
    path, re_path
)

from . import views

# app_name = 'member'

urlpatterns = [
    # Account
    path('login/',
         views.MemberLoginView.as_view(), name="account_login"),
    path('logout/',
         views.MemberLogoutView.as_view(), name="account_logout"),

    # Social Providers
    path('social/login/cancelled/',
         views.MemberSocialLoginCancelledView.as_view(), name='socialaccount_login_cancelled'),
    path('social/login/error/',
         views.MemberSocialLoginErrorView.as_view(), name='socialaccount_login_error'),
    path('social/signup/',
         views.MemberSocialSignupView.as_view(), name='socialaccount_signup'),
    path('social/connections/',
         views.MemberSocialConnectionsView.as_view(), name='socialaccount_connections'),

    # Email Confirmation
    path('confirm-email/',
         views.MemberEmailVerificationSentView.as_view(), name="account_email_verification_sent"),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$',
            views.MemberConfirmEmailView.as_view(), name="account_confirm_email"),
    path('email/',
         views.MemberEmailView.as_view(), name="account_email"),
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
