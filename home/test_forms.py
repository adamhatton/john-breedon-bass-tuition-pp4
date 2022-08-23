from django.test import TestCase
from .forms import ContactForm


class TestContactForm(TestCase):
    '''
    Class for testing the Contact Form
    '''

    def test_contact_name_is_required(self):
        '''Tests that name is required in contact form'''
        form = ContactForm({
            'name': '',
            'email': 'test@test.co.uk',
            'phone': '',
            'message': 'testing'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())

    def test_contact_email_is_required(self):
        '''Tests that email is required in contact form'''
        form = ContactForm({
            'name': 'Adam',
            'email': '',
            'phone': '',
            'message': 'testing'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

    def test_contact_message_is_required(self):
        '''Tests that message is required in contact form'''
        form = ContactForm({
            'name': 'Adam',
            'email': 'test@test.co.uk',
            'phone': '',
            'message': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors.keys())

    def test_phone_field_validation(self):
        '''Tests that validation is shown if an incorrect phone number is
        entered'''
        form = ContactForm({
            'name': 'Adam',
            'email': 'test@test.co.uk',
            'phone': '12345',
            'message': 'testing'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors.keys())

    def test_fields_are_explicit_in_form_metaclass(self):
        '''Tests that only fields specified in the meta are displayed'''
        form = ContactForm()
        self.assertEqual(
            form.Meta().fields,
            ('name', 'email', 'phone', 'message')
        )

