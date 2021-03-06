from allauth.account import views as allauth_views
from allauth.socialaccount import views as socialaccount_views
from django.contrib.auth import mixins as auth_mixins
from django.utils.translation import gettext_lazy as _
from django.views import generic

from . import forms

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


class MemberSocialLoginCancelledView(socialaccount_views.LoginCancelledView):
    template_name = 'member/socialaccount/login_cancelled.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialLoginCancelledView, self).get_context_data(**kwargs)
        context['page_title'] = _('Login Cancelled')
        return context


class MemberSocialLoginErrorView(socialaccount_views.LoginErrorView):
    template_name = 'member/socialaccount/authentication_error.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialLoginErrorView, self).get_context_data(**kwargs)
        context['page_title'] = _('Social Network Login Failure')
        return context


class MemberSocialSignupView(socialaccount_views.SignupView):
    template_name = 'member/socialaccount/signup.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialSignupView, self).get_context_data(**kwargs)
        context['page_title'] = _('Sign Up')
        return context


class MemberSocialConnectionsView(auth_mixins.LoginRequiredMixin, socialaccount_views.ConnectionsView):
    template_name = 'member/socialaccount/connections.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialConnectionsView, self).get_context_data(**kwargs)
        context['page_title'] = _('Connect with SNS accounts')
        return context


class MemberEmailVerificationSentView(allauth_views.EmailVerificationSentView):
    template_name = 'member/account/verification_sent.html'

    def get_context_data(self, **kwargs):
        context = super(MemberEmailVerificationSentView, self).get_context_data(**kwargs)
        context['page_title'] = _('Email Verification Sent')
        return context


class MemberConfirmEmailView(allauth_views.ConfirmEmailView):
    template_name = 'member/account/email_confirm.html'

    def get_context_data(self, **kwargs):
        context = super(MemberConfirmEmailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Confirm Email Request')
        return context


class MemberEmailView(auth_mixins.LoginRequiredMixin, allauth_views.EmailView):
    template_name = 'member/account/email.html'
    form_class = forms.MemberAddEmailForm

    def get_context_data(self, **kwargs):
        context = super(MemberEmailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Email Management')
        return context