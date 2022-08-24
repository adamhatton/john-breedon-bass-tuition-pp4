from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import LearnerProfile, Testimonial
from bookings.models import Booking


class TestLearnerAccountViews(TestCase):
    '''
    Class for testing the learner_account views
    '''

    def setUp(self):
        '''Creates a user, booking, date and testimonial to use in all tests'''
        username = 'adhatton'
        password = 'adam'
        user = get_user_model()
        test_user = user.objects.create_user(
            username=username,
            password=password,
        )
        tomorrow = datetime.now() + timedelta(days=2)
        Booking.objects.create(
            user=test_user,
            date=tomorrow,
            time='10',
            type='O',
        )
        Testimonial.objects.create(
            user=test_user,
            content='test testimonial',
            approved=True
        )

    def test_get_account_page_if_not_logged_in(self):
        '''Tests that the account page redirects if not logged in'''
        response = self.client.get('/learner_account/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/learner_account/')

    def test_get_account_page_logged_in(self):
        '''Tests that the account page uses correct template if logged in'''
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('learner_account'))
        self.assertEqual(str(response.context['user']), 'adhatton')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('learner_account.html')

    def test_render_bookings_and_testimonials(self):
        '''Tests that the account page renders bookings and testimonials'''
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('learner_account'))
        assert b'test testimonial' in response.content
        assert b'10:00 - 11:00' in response.content

    def test_render_no_bookings_message(self):
        '''Tests that the account page renders the no bookings message'''
        Booking.objects.filter(pk=1).delete()
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('learner_account'))
        assert b'You currently have no bookings' in response.content

    def test_render_approval_message(self):
        '''
        Tests that the account page renders the testimonial
        approval message
        '''
        test_test = Testimonial.objects.get(pk=1)
        test_test.approved = False
        test_test.save()
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('learner_account'))
        assert b'Your testimonial is awaiting approval' in response.content

    def test_send_valid_user_and_profile_form(self):
        '''
        Tests that sending a valid user form and profile form
        updates the model, renders the learner_account template
        and shows a message
        '''
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(reverse('learner_account'), {
            'username': 'adhatton',
            'first_name': 'adam',
            'last_name': 'hatton',
            'email': 'test@test.co.uk',
            'phone': '07450039175',
            'ability': 'B',
            'about': 'I like music'
        }, follow=True)
        messages = list(response.context['messages'])
        user = User.objects.get(pk=1)
        self.assertRedirects(response, '/learner_account/')
        self.assertEqual(user.first_name, 'adam')
        self.assertEqual(user.last_name, 'hatton')
        self.assertEqual(user.email, 'test@test.co.uk')
        self.assertEqual(user.learnerprofile.phone, '07450039175')
        self.assertEqual(user.learnerprofile.ability, 'B')
        self.assertEqual(user.learnerprofile.about, 'I like music')
        self.assertTemplateUsed('learner_account.html')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile successfully updated')

    def test_send_invalid_user_and_profile_form(self):
        '''
        Tests that sending an invalid profile form renders the learner_account
        template and does not update the model
        '''
        self.client.login(username='adhatton', password='adam')
        self.client.post(reverse('learner_account'), {
            'username': ''
        })
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, 'adhatton')
        self.assertTemplateUsed('learner_account.html')

    def test_get_add_testimonial_if_not_logged_in(self):
        '''Tests that the add testimonial page redirects if not logged in'''
        response = self.client.get(reverse('add_testimonial'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/learner_account/add_testimonial/')

    def test_get_add_testimonial_if_logged_in(self):
        '''
        Tests that the add testimonial page GET method
        redirects if logged in
        '''
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('add_testimonial'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/learner_account/')

    def test_post_add_testimonial(self):
        '''
        Tests that the add testimonial page POST method adds a testimonial
        to the DB, redirects to learner_account and shows a message
        '''
        Testimonial.objects.filter(pk=1).delete()
        test_user = User.objects.get(pk=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('add_testimonial'),
            {'content': 'test of POST testimonial'},
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(
            test_user.testimonial.content,
            'test of POST testimonial'
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/learner_account/')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Testimonial has been sent for approval')

    def test_get_edit_testimonial_if_not_logged_in(self):
        '''Tests that the edit testimonial page redirects if not logged in'''
        response = self.client.get(reverse('edit_testimonial'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/learner_account/edit_testimonial/')

    def test_get_edit_testimonial_if_logged_in(self):
        '''
        Tests that the edit testimonial page GET method
        redirects if logged in
        '''
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('edit_testimonial'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/learner_account/')

    def test_post_edit_testimonial(self):
        '''
        Tests that the edit testimonial page POST method edits a testimonial
        in the DB, redirects to learner_account and shows a message
        '''
        test_user = User.objects.get(pk=1)
        self.client.login(username='adhatton', password='adam')
        response = self.client.post(
            reverse('edit_testimonial'),
            {'content': 'test of POST edit testimonial'},
            follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(
            test_user.testimonial.content,
            'test of POST edit testimonial'
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/learner_account/')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Testimonial has been sent for approval')

    def test_get_delete_testimonial_if_not_logged_in(self):
        '''Tests that the delete testimonial page redirects if not logged in'''
        response = self.client.get(reverse('delete_testimonial'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/learner_account/delete_testimonial/')

    def test_get_delete_testimonial_if_logged_in(self):
        '''
        Tests that the delete testimonial page GET method deletes the
        Testimonial if logged in and redirects to learner_account
        '''
        self.client.login(username='adhatton', password='adam')
        response = self.client.get(reverse('delete_testimonial'), follow=True)
        messages = list(response.context['messages'])
        self.assertFalse(Testimonial.objects.filter(pk=1).exists())
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/learner_account/')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Testimonial successfully deleted')