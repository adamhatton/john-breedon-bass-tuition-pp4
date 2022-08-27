from django.test import TestCase
from .forms import BookingForm


class TestBookingForm(TestCase):
    '''
    Class for testing the Booking Form
    '''

    def test_booking_required_fields(self):
        '''Tests that date, time and type are required in booking form'''
        form = BookingForm({
            'date': '',
            'time': '',
            'type': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors.keys())
        self.assertIn('time', form.errors.keys())
        self.assertIn('type', form.errors.keys())

    def test_booking_fields_are_explicit_in_form_metaclass(self):
        '''Tests that only fields specified in the meta are displayed'''
        form = BookingForm()
        self.assertEqual(
            form.Meta().fields,
            ('date', 'time', 'phone', 'type')
        )

    def test_booking_date_field_uses_date_widget(self):
        '''Tests that the date field uses a date widget'''
        form = BookingForm()
        self.assertEqual(
            form.fields['date'].widget.__class__.__name__,
            'DateInput'
        )
