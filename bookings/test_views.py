from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Booking


class TestBookingsPageView(TestCase):
    '''
    Class for testing the BookingsPage class view
    '''

    def setUp(self):
        '''Creates a user and date to use in all tests'''
        username = 'adhatton'
        password = 'adam'
        user = get_user_model()
        user.objects.create_user(
            username=username,
            password=password,
        )

    def test_get_bookings_page_if_not_logged_in(self):
        '''Tests that the bookings page redirects if not logged in'''
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/bookings/')

    def test_get_bookings_page_logged_in(self):
        '''Tests that the bookings page uses correct template if logged in'''
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('bookings'))
        self.assertEqual(str(response.context['user']), 'adhatton')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')

    def test_render_booking_availability(self):
        '''Tests that the bookings page renders booked slots as BOOKED'''
        test_user = User.objects.get(pk=1)
        tomorrow = datetime.now() + timedelta(days=1)
        Booking.objects.create(
            user=test_user,
            date=tomorrow,
            time='10',
            type='O'
        )
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('bookings'))
        assert b'BOOKED' in response.content

    def test_post_booking_rejects_duplicate_booking(self):
        '''Tests that the booking POST method prevents duplicate bookings'''
        test_user = User.objects.get(pk=1)
        tomorrow = datetime.now() + timedelta(days=1)
        Booking.objects.create(
            user=test_user,
            date=tomorrow,
            time='10',
            type='O'
        )
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('bookings'),
            {
                'date': f'{tomorrow.strftime("%Y-%m-%d")}',
                'time': '10',
                'type': 'O'
            },
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'That slot is unavailable, please select a different time'
        )
        self.assertRedirects(response, reverse('bookings'))
        self.assertTemplateUsed(response, 'bookings.html')

    def test_post_booking_accepts_new_bookings(self):
        '''Tests that the booking POST method accepts new bookings'''
        tomorrow = datetime.now() + timedelta(days=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('bookings'),
            {
                'date': f'{tomorrow.strftime("%Y-%m-%d")}',
                'time': '10',
                'type': 'O'
            },
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your lesson is booked!')
        self.assertRedirects(response, reverse('bookings'))
        self.assertTemplateUsed(response, 'bookings.html')
        self.assertTrue(Booking.objects.filter(time='10').exists())

    def test_post_booking_redirects_invalid_bookings(self):
        '''
        Tests that when user tries to POST an invalid booking that the
        bookings page is re-rendered
        '''
        tomorrow = datetime.now() + timedelta(days=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('bookings'),
            {
                'date': f'{tomorrow.strftime("%Y-%m-%d")}',
                'time': '10',
                'phone': '12345',
                'type': 'O'
            },
        )
        self.assertTemplateUsed(response, 'bookings.html')


class TestEditBookingView(TestCase):
    '''
    Class for testing the EditBooking class view
    '''

    def setUp(self):
        '''Creates a user and date to use in all tests'''
        username = 'adhatton'
        password = 'adam'
        user = get_user_model()
        test_user = user.objects.create_user(
            username=username,
            password=password,
        )
        tomorrow = datetime.now() + timedelta(days=1)
        Booking.objects.create(
            user=test_user,
            date=tomorrow,
            time='10',
            type='O'
        )

    def test_get_edit_booking_page_redirects_if_not_logged_in(self):
        '''Tests that the edit booking page redirects if not logged in'''
        booking = Booking.objects.get(pk=1)
        response = self.client.get(reverse('edit_booking', args=[booking.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/bookings/edit_booking/{booking.pk}/'
        )

    def test_get_edit_booking_page_if_logged_in(self):
        '''
        Tests that the edit booking page renders correct template if
        user is logged in
        '''
        booking = Booking.objects.get(pk=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('edit_booking', args=[booking.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')

    def test_get_edit_booking_redirects_if_other_user_booking(self):
        '''
        Tests that the edit booking page redirects to the learner account
        page if a user tries to edit a booking which isn't their own
        '''
        booking = Booking.objects.get(pk=1)
        User.objects.create_user(
            username='wronguser',
            password='wrong',
        )
        self.client.login(username='wronguser', password='wrong')
        response = self.client.get(reverse('edit_booking', args=[booking.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('learner_account'))

    def test_edit_booking_updates_booking(self):
        '''
        Tests that the edit booking POST method updates
        the booking object
        '''
        booking = Booking.objects.get(pk=1)
        tomorrow = datetime.now() + timedelta(days=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('edit_booking', args=[booking.pk]),
            {
                'date': f'{tomorrow.strftime("%Y-%m-%d")}',
                'time': '13',
                'type': 'S'
            },
            follow=True
        )
        updated_booking = Booking.objects.get(pk=1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Your lesson has been successfully changed!'
        )
        self.assertRedirects(response, reverse('learner_account'))
        self.assertTemplateUsed(response, 'learner_account.html')
        self.assertEqual(updated_booking.time, '13')
        self.assertEqual(updated_booking.type, 'S')

    def test_edit_booking_rejects_duplicate_booking(self):
        '''
        Tests that the edit booking POST method prevents booking onto
        a booked slot that is not the slot being edited
        '''
        day_after_tomorrow = datetime.now() + timedelta(days=2)
        test_user = User.objects.get(pk=1)
        Booking.objects.create(
            user=test_user,
            date=day_after_tomorrow,
            time='10',
            type='O'
        )
        booking = Booking.objects.get(pk=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('edit_booking', args=[booking.pk]),
            {
                'date': f'{day_after_tomorrow.strftime("%Y-%m-%d")}',
                'time': '10',
                'type': 'O'
            },
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'That slot is unavailable, please select a different time'
        )
        self.assertRedirects(
            response,
            reverse('edit_booking', args=[booking.pk])
        )
        self.assertTemplateUsed(response, 'bookings.html')

    def test_edit_booking_allows_type_update_only(self):
        '''
        Tests that the edit booking POST method allows a user to
        edit just the lesson type on an existing booking
        '''
        tomorrow = datetime.now() + timedelta(days=1)
        booking = Booking.objects.get(pk=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('edit_booking', args=[booking.pk]),
            {
                'date': f'{tomorrow.strftime("%Y-%m-%d")}',
                'time': '10',
                'type': 'H'
            },
            follow=True
        )
        updated_booking = Booking.objects.get(pk=1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Your lesson has been successfully changed!'
        )
        self.assertRedirects(
            response,
            reverse('learner_account')
        )
        self.assertTemplateUsed(response, 'learner_account.html')
        self.assertEqual(updated_booking.time, '10')
        self.assertEqual(updated_booking.type, 'H')

    def test_edit_booking_invalid_bookings(self):
        '''
        Tests that when user tries to POST an invalid booking to the edit
        view that the bookings page is re-rendered
        '''
        booking = Booking.objects.get(pk=1)
        tomorrow = datetime.now() + timedelta(days=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('edit_booking', args=[booking.pk]),
            {
                'date': f'{tomorrow.strftime("%Y-%m-%d")}',
                'time': '15',
                'phone': '12345',
                'type': 'O'
            },
        )
        self.assertTemplateUsed(response, 'bookings.html')


class TestDeleteBookingView(TestCase):
    '''
    Class for testing the delete booking view
    '''

    def setUp(self):
        '''Creates a user and date to use in all tests'''
        username = 'adhatton'
        password = 'adam'
        user = get_user_model()
        test_user = user.objects.create_user(
            username=username,
            password=password,
        )
        tomorrow = datetime.now() + timedelta(days=1)
        Booking.objects.create(
            user=test_user,
            date=tomorrow,
            time='10',
            type='O'
        )

    def test_get_delete_booking_if_not_logged_in(self):
        '''Tests that the del booking page redirects if not logged in'''
        booking = Booking.objects.get(pk=1)
        response = self.client.get(
            reverse('delete_booking', args=[booking.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/bookings/delete_booking/1/'
        )

    def test_get_delete_booking_if_logged_in(self):
        '''
        Tests that the delete booking page GET method deletes the
        booking if logged in and redirects to learner_account
        '''
        booking = Booking.objects.get(pk=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(
            reverse('delete_booking', args=[booking.pk]),
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertFalse(Booking.objects.filter(pk=1).exists())
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('learner_account'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Booking successfully deleted')

    def test_get_delete_redirects_if_wrong_user(self):
        '''
        Tests that the delete booking page GET method redirects if
        a user tries to delete another user's booking
        '''
        booking = Booking.objects.get(pk=1)
        User.objects.create_user(
            username='wronguser',
            password='wrong',
        )
        self.client.login(username='wronguser', password='wrong')
        response = self.client.get(
            reverse('delete_booking', args=[booking.pk]),
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertTrue(Booking.objects.filter(pk=1).exists())
        self.assertRedirects(response, reverse('learner_account'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'You do not have permission to delete that booking'
        )
