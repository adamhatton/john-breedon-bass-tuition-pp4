from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Button, Field, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import LearnerProfile, Testimonial


class UserForm(forms.ModelForm):
    """
    Creates an instance of the UserForm to be passed to a template
    """

    # Create layout variables for use with crispy forms
    disabled_layout = Layout(
        FloatingField("username", disabled=True),
        FloatingField("first_name", disabled=True),
        FloatingField("last_name", disabled=True),
        FloatingField("email", disabled=True),
    )
    enabled_layout = Layout(
        FloatingField("username"),
        FloatingField("first_name"),
        FloatingField("last_name"),
        FloatingField("email"),
    )

    class Meta:
        """
        Specifies the fields to be included in the UserForm class
        """

        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        """
        Creates a FormHelper to enable layout changes in crispy forms
        """
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = self.disabled_layout


class LearnerProfileForm(forms.ModelForm):
    """
    Creates an instance of the ProfileForm to be passed to a template
    """

    # Create layout variables for use with crispy forms
    disabled_layout = Layout(
        FloatingField("phone", disabled=True),
        FloatingField("ability", disabled=True),
        Field("about", disabled=True),
        Div(
            HTML(
                '<a class="btn btn-secondary hidden" id="button-id-cancel" '
                'href="{% url "learner_account" %}">&laquo; Cancel</a>'
            ),
            Button("edit", "Edit", css_class="btn-secondary"),
            Submit("submit", "Submit", disabled=True),
            css_class="center-button",
        ),
    )

    enabled_layout = Layout(
        FloatingField("phone"),
        FloatingField("ability"),
        Field("about"),
        Div(
            HTML(
                '<a class="btn btn-secondary" id="button-id-cancel" '
                'href="{% url "learner_account" %}">&laquo; Cancel</a>'
            ),
            Button("edit", "Edit", css_class="btn-secondary hidden"),
            Submit("submit", "Submit"),
            css_class="center-button",
        ),
    )

    class Meta:
        """
        Specifies the fields to be included in the LearnerProfileForm class
        """

        model = LearnerProfile
        fields = ("phone", "ability", "about")

    def __init__(self, *args, **kwargs):
        """
        Creates a FormHelper to enable layout changes in crispy forms
        """
        super(LearnerProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = self.disabled_layout


class TestimonialForm(forms.ModelForm):
    """
    Creates an instance of the ProfileForm to be passed to a template
    """

    class Meta:
        """
        Specifies the fields to be included in the TestimonialForm class
        """

        model = Testimonial
        fields = ("content",)

    def __init__(self, *args, **kwargs):
        """
        Creates a FormHelper to enable layout changes in crispy forms
        """
        super(TestimonialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_show_labels = False
