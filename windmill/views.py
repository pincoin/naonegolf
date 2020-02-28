from django.utils import timezone
from django.views import generic

from . import forms
from . import models


class TeeOffListView(generic.ListView):
    context_object_name = 'days'

    template_name = 'windmill/tee_off_list.html'

class BookingCreateForm(generic.CreateView):

    template_name = 'windmill/booking_create.html'
