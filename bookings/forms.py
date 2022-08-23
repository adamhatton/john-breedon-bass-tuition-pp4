import datetime
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
import availability
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Creates an instance of the BookingForm to be passed to a template
    """
    class Meta:
        """
        Specifies the fields to be included in the UserForm class
        """

        model = Booking
        fields = ("date", "time", "phone", "type")
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": (
                        availability.get_next_7_days(datetime.date.today())[0]
                    ),
                    "max": (
                        availability.get_next_7_days(datetime.date.today())[6]
                    ),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Creates a FormHelper to enable layout changes in crispy forms
        """
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("date"),
            FloatingField("time"),
            FloatingField("phone"),
            FloatingField("type"),
            Submit("booking-submit", "Submit"),
        )
