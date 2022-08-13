from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import LearnerProfile


class UserForm(forms.ModelForm):
    '''
    Creates an instance of the UserForm to be passed to a template
    '''
    class Meta:
        '''
        Specifies the fields to be included in the UserForm class
        '''
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        '''
        Creates a FormHelper to enable layout changes in crispy forms
        '''
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('first_name'),
            FloatingField('last_name', placeholder="Surname"),
            FloatingField('email'),
        )


class LearnerProfileForm(forms.ModelForm):
    '''
    Creates an instance of the ProfileForm to be passed to a template
    '''
    class Meta:
        '''
        Specifies the fields to be included in the LearnerProfileForm class
        '''
        model = LearnerProfile
        fields = ('phone', 'ability', 'about')

    def __init__(self, *args, **kwargs):
        '''
        Creates a FormHelper to enable layout changes in crispy forms
        '''
        super(LearnerProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            FloatingField('phone'),
            FloatingField('ability'),
            'about',
            'message',
        )
