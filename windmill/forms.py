from django import forms
from django.utils import timezone

from . import models


class BookingAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)

    class Meta:
        model = models.Booking
        exclude = ()
