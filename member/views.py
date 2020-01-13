from allauth.account import views as allauth_views
from django.utils.translation import gettext_lazy as _


class MemberLoginView(allauth_views.LoginView):
    template_name = 'member/account/login.html'

    def get_context_data(self, **kwargs):
        context = super(MemberLoginView, self).get_context_data(**kwargs)
        context['page_title'] = _('Login')

        return context
