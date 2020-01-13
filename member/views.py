from django.utils.translation import gettext_lazy as _
from django.views import generic


class MemberLoginView(generic.TemplateView):
    template_name = 'member/account/login.html'

    def get_context_data(self, **kwargs):
        context = super(MemberLoginView, self).get_context_data(**kwargs)
        context['page_title'] = _('Login')

        return context
