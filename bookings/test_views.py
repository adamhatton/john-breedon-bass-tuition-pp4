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
        test_user = user.objects.create_user(
            username=username,
            password=password,
        )

    def test_get_bookings_page_if_not_logged_in(self):
        '''Tests that the bookings page redirects if not logged in'''
        response = self.client.get('/bookings/')
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
            {'date': f'{tomorrow.strftime("%Y-%m-%d")}', 'time': '10', 'type': 'O'},
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'That slot is unavailable, please select a different time')
        self.assertRedirects(response, '/bookings/')
        self.assertTemplateUsed(response, 'bookings.html')

    def test_post_booking_accepts_new_bookings(self):
        '''Tests that the booking POST method accepts new bookings'''
        tomorrow = datetime.now() + timedelta(days=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('bookings'),
            {'date': f'{tomorrow.strftime("%Y-%m-%d")}', 'time': '10', 'type': 'O'},
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your lesson is booked!')
        self.assertRedirects(response, '/bookings/')
        self.assertTemplateUsed(response, 'bookings.html')
        self.assertTrue(Booking.objects.filter(time='10').exists())

    def test_post_booking_redirects_invalid_bookings(self):
        '''
        Tests that when user tries to POST and invalid booking that the
        bookings page is re-rendered
        '''
        tomorrow = datetime.now() + timedelta(days=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('bookings'),
            {'date': f'{tomorrow.strftime("%Y-%m-%d")}', 'time': '10', 'phone': '12345', 'type': 'O'},
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
        response = self.client.get(f'/bookings/edit_booking/{booking.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/bookings/edit_booking/{booking.pk}/')

    def test_get_edit_booking_page_if_logged_in(self):
        '''
        Tests that the edit booking page renders correct template if
        user is logged in
        '''
        booking = Booking.objects.get(pk=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(f'/bookings/edit_booking/{booking.pk}/')
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
        response = self.client.get(f'/bookings/edit_booking/{booking.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/learner_account/')

    def test_edit_booking_updates_booking(self):
        '''
        Tests that the edit booking POST method updates
        the booking object
        '''
        booking = Booking.objects.get(pk=1)
        tomorrow = datetime.now() + timedelta(days=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            f'/bookings/edit_booking/{booking.pk}/',
            {'date': f'{tomorrow.strftime("%Y-%m-%d")}', 'time': '13', 'type': 'S'},
            follow=True
        )
        updated_booking = Booking.objects.get(pk=1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your lesson has been successfully changed!')
        self.assertRedirects(response, '/learner_account/')
        self.assertTemplateUsed(response, 'learner_account.html')
        self.assertEqual(updated_booking.time, '13')
        self.assertEqual(updated_booking.type, 'S')

    # def test_post_booking_redirects_invalid_bookings(self):
    #     '''
    #     Tests that when user tries to POST and invalid booking that the
    #     bookings page is re-rendered
    #     '''
    #     tomorrow = datetime.now() + timedelta(days=1)
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.post(
    #         reverse('bookings'),
    #         {'date': f'{tomorrow.strftime("%Y-%m-%d")}', 'time': '10', 'phone': '12345', 'type': 'O'},
    #     )
    #     self.assertTemplateUsed(response, 'bookings.html')


    # def test_render_no_bookings_message(self):
    #     '''Tests that the account page renders the no bookings message'''
    #     Booking.objects.filter(pk=1).delete()
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.get(reverse('learner_account'))
    #     assert b'You currently have no bookings' in response.content

    # def test_render_approval_message(self):
    #     '''
    #     Tests that the account page renders the testimonial
    #     approval message
    #     '''
    #     test_test = Testimonial.objects.get(pk=1)
    #     test_test.approved = False
    #     test_test.save()
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.get(reverse('learner_account'))
    #     assert b'Your testimonial is awaiting approval' in response.content

    # def test_send_valid_user_and_profile_form(self):
    #     '''
    #     Tests that sending a valid user form and profile form
    #     updates the model, renders the learner_account template
    #     and shows a message
    #     '''
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.post(reverse('learner_account'), {
    #         'username': 'adhatton',
    #         'first_name': 'adam',
    #         'last_name': 'hatton',
    #         'email': 'test@test.co.uk',
    #         'phone': '07450039175',
    #         'ability': 'B',
    #         'about': 'I like music'
    #     }, follow=True)
    #     messages = list(response.context['messages'])
    #     user = User.objects.get(pk=1)
    #     self.assertRedirects(response, '/learner_account/')
    #     self.assertEqual(user.first_name, 'adam')
    #     self.assertEqual(user.last_name, 'hatton')
    #     self.assertEqual(user.email, 'test@test.co.uk')
    #     self.assertEqual(user.learnerprofile.phone, '07450039175')
    #     self.assertEqual(user.learnerprofile.ability, 'B')
    #     self.assertEqual(user.learnerprofile.about, 'I like music')
    #     self.assertTemplateUsed('learner_account.html')
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'Profile successfully updated')

    # def test_send_invalid_user_and_profile_form(self):
    #     '''
    #     Tests that sending an invalid profile form renders the learner_account
    #     template and does not update the model
    #     '''
    #     self.client.login(username='adhatton', password='adam')
    #     self.client.post(reverse('learner_account'), {
    #         'username': ''
    #     })
    #     user = User.objects.get(pk=1)
    #     self.assertEqual(user.username, 'adhatton')
    #     self.assertTemplateUsed('learner_account.html')

    # def test_get_add_testimonial_if_not_logged_in(self):
    #     '''Tests that the add testimonial page redirects if not logged in'''
    #     response = self.client.get(reverse('add_testimonial'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/accounts/login/?next=/learner_account/add_testimonial/')

    # def test_get_add_testimonial_if_logged_in(self):
    #     '''
    #     Tests that the add testimonial page GET method
    #     redirects if logged in
    #     '''
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.get(reverse('add_testimonial'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/learner_account/')

    # def test_post_add_testimonial(self):
    #     '''
    #     Tests that the add testimonial page POST method adds a testimonial
    #     to the DB, redirects to learner_account and shows a message
    #     '''
    #     Testimonial.objects.filter(pk=1).delete()
    #     test_user = User.objects.get(pk=1)
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.post(
    #         reverse('add_testimonial'),
    #         {'content': 'test of POST testimonial'},
    #         follow=True
    #     )
    #     messages = list(response.context['messages'])
    #     self.assertEqual(
    #         test_user.testimonial.content,
    #         'test of POST testimonial'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, '/learner_account/')
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'Testimonial has been sent for approval')

    # def test_get_edit_testimonial_if_not_logged_in(self):
    #     '''Tests that the edit testimonial page redirects if not logged in'''
    #     response = self.client.get(reverse('edit_testimonial'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/accounts/login/?next=/learner_account/edit_testimonial/')

    # def test_get_edit_testimonial_if_logged_in(self):
    #     '''
    #     Tests that the edit testimonial page GET method
    #     redirects if logged in
    #     '''
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.get(reverse('edit_testimonial'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/learner_account/')

    # def test_post_edit_testimonial(self):
    #     '''
    #     Tests that the edit testimonial page POST method edits a testimonial
    #     in the DB, redirects to learner_account and shows a message
    #     '''
    #     test_user = User.objects.get(pk=1)
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.post(
    #         reverse('edit_testimonial'),
    #         {'content': 'test of POST edit testimonial'},
    #         follow=True
    #     )
    #     messages = list(response.context['messages'])
    #     self.assertEqual(
    #         test_user.testimonial.content,
    #         'test of POST edit testimonial'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, '/learner_account/')
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'Testimonial has been sent for approval')

    # def test_get_delete_testimonial_if_not_logged_in(self):
    #     '''Tests that the delete testimonial page redirects if not logged in'''
    #     response = self.client.get(reverse('delete_testimonial'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, '/accounts/login/?next=/learner_account/delete_testimonial/')

    # def test_get_delete_testimonial_if_logged_in(self):
    #     '''
    #     Tests that the delete testimonial page GET method deletes the
    #     Testimonial if logged in and redirects to learner_account
    #     '''
    #     self.client.login(username='adhatton', password='adam')
    #     response = self.client.get(reverse('delete_testimonial'), follow=True)
    #     messages = list(response.context['messages'])
    #     self.assertFalse(Testimonial.objects.filter(pk=1).exists())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, '/learner_account/')
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'Testimonial successfully deleted')