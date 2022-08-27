from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Booking


class TestBookingModel(TestCase):
    '''Class for testing the Booking Model'''

    def setUp(self):
        '''Create a user object and booking object to use in all tests'''
        test_user = User.objects.create(
            username='adhatton',
            password='password',
        )
        tomorrow = datetime.now() + timedelta(days=1)
        Booking.objects.create(
            user=test_user,
            date=tomorrow,
            time='10',
            type='O'
        )

    def test_time_max_length(self):
        '''Test that time field has max length of 2'''
        booking = Booking.objects.get(pk=1)
        max_length = booking._meta.get_field('time').max_length
        self.assertEqual(max_length, 2)

    def test_type_max_length(self):
        '''Test that type field has max length of 1'''
        booking = Booking.objects.get(pk=1)
        max_length = booking._meta.get_field('type').max_length
        self.assertEqual(max_length, 1)

    def test_booking_str_method(self):
        '''Test the string method returns expected string'''
        booking = Booking.objects.get(pk=1)
        expected_string = (
            f'Lesson on {booking.date.strftime("%a %d %B")} at {booking.time}'
        )
        self.assertEqual(str(booking), expected_string)
