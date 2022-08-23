from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserForm, LearnerProfileForm, TestimonialForm


class TestUserForm(TestCase):
    '''
    Class for testing the User Form
    '''

    def test_user_required_fields(self):
        '''Tests that username and email are required in user form'''
        form = UserForm({
            'username': '',
            'email': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())
        self.assertIn('email', form.errors.keys())

    def test_user_fields_are_explicit_in_form_metaclass(self):
        '''Tests that only fields specified in the meta are displayed'''
        form = UserForm()
        self.assertEqual(
            form.Meta().fields,
            ('username', 'first_name', 'last_name', 'email')
        )


class TestLearnerProfileForm(TestCase):
    '''
    Class for testing the LearnerProfile Form
    '''

    def test_learner_profile_required_fields(self):
        '''Tests that none of the fields in LearnerProfile form are required'''
        test_user = User.objects.create(
            username='adhatton',
            password='adam',
        )
        form = LearnerProfileForm({'user': test_user})
        self.assertTrue(form.is_valid())

    def test_learner_profile_fields_are_explicit_in_form_metaclass(self):
        '''Tests that only fields specified in the meta are displayed'''
        form = LearnerProfileForm()
        self.assertEqual(
            form.Meta().fields,
            ('phone', 'ability', 'about')
        )


class TestTestimonialForm(TestCase):
    '''
    Class for testing the Testimonial Form
    '''

    def test_testimonial_required_fields(self):
        '''Tests that the content field is required'''
        form = TestimonialForm({'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors.keys())

    def test_testimonial_fields_are_explicit_in_form_metaclass(self):
        '''Tests that only fields specified in the meta are displayed'''
        form = TestimonialForm()
        self.assertEqual(
            form.Meta().fields,
            ('content',)
        )
