from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        '''
        Specifies the fields to be included in the UserForm class
        '''
        model = Booking
        fields = ('date', 'time', 'phone', 'type')