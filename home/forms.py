from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Creates an instance of the ContactForm to be passed to a template
    """

    class Meta:
        """
        Specifies the fields to be included in the ContactForm class
        """

        model = Contact
        fields = ("name", "email", "phone", "message")

    def __init__(self, *args, **kwargs):
        """
        Creates a FormHelper to enable layout changes in crispy forms
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("name"),
            FloatingField("email"),
            FloatingField("phone"),
            "message",
            Div(Submit("submit", "Submit"), css_class="center-button"),
        )
