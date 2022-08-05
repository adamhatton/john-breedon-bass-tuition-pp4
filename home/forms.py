from .models import Contact
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField

class ContactForm(forms.ModelForm):
    '''
    Creates an instance of the ContactForm to be passed to a template
    '''

    class Meta:
        '''
        Specifies the fields to be included in the ContactForm class
        '''
        model = Contact
        fields = ('name', 'email', 'phone', 'message')
    

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            FloatingField('name'),
            FloatingField('email'),
            FloatingField('phone', placeholder='Phone [not required]'),
            'message',
            Div (
                Submit('submit', 'Submit'),
                css_id = 'contact-submit'
            ),
        )