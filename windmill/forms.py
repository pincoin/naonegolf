from django import forms

from . import models


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = [
            'round_time', 'pax', 'hole',
            'green_fee_sales', 'caddie_fee_sales', 'cart_fee_sales',
            'green_fee_pay_on_arrival', 'caddie_fee_pay_on_arrival', 'cart_fee_pay_on_arrival',
            'green_fee_cost', 'caddie_fee_cost', 'cart_fee_cost', 'cart_fee_deducted_from_deposit',
            'first_name', 'last_name', 'memo',
            'season', 'day_of_week', 'slot', 'stand_by',
        ]

    def clean(self):
        pass
