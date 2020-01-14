from allauth.account import views as allauth_views
from django.utils.translation import gettext_lazy as _
from django.views import generic


class MemberLoginView(generic.TemplateView):
    template_name = 'member/account/login.html'

    def get_context_data(self, **kwargs):
        context = super(MemberLoginView, self).get_context_data(**kwargs)
        context['page_title'] = _('Sign In')
        return context


class MemberLogoutView(allauth_views.LogoutView):
    template_name = 'member/account/logout.html'

    def get_context_data(self, **kwargs):
        context = super(MemberLogoutView, self).get_context_data(**kwargs)
        context['page_title'] = _('Sign Out')
        return context
