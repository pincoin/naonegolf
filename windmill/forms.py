from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class TeeOffTimeAdminForm(forms.ModelForm):
    sales = forms.FloatField(
        label=_('Sales'),
        required=False,
    )

    profit = forms.FloatField(
        label=_('Profit'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(TeeOffTimeAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.TeeOffTime
        fields = '__all__'
