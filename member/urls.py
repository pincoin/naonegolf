from importlib import import_module

from allauth.socialaccount import providers

app_name = 'member'

urlpatterns = [
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