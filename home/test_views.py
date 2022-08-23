from django.test import TestCase
from django.contrib.auth.models import User
from .models import Contact
from learner_account.models import Testimonial


class TestHomeViews(TestCase):
    '''
    Class for testing the home views
    '''

    def test_get_index_redirects(self):
        '''Tests that the index page redirects to the home page'''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')

    def test_get_home(self):
        '''Tests that the home page renders the correct template'''
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_contact(self):
        '''Tests that the contact page renders the correct template'''
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_send_valid_contact_form(self):
        '''
        Tests that sending a valid contact form creates a contact,
        renders the homepage template and shows a message
        '''
        response = self.client.post('/contact/', data={
            'name': 'Adam',
            'email': 'test@test.co.uk',
            'phone': '',
            'message': 'testing'
        })
        messages = list(response.context['messages'])
        self.assertTrue(Contact.objects.all().exists())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Message sent successfully')

    def test_send_invalid_contact_form(self):
        '''
        Tests that sending an invalid contact form does not create
        a contact item and renders the homepage template
        '''
        response = self.client.post('/contact/', data={
            'name': '',
            'email': 'test@test.co.uk',
            'phone': '',
            'message': 'testing'
        })
        self.assertFalse(Contact.objects.all().exists())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_about(self):
        '''Tests that the about page renders the correct template'''
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_about_displays_testimonial(self):
        '''
        Tests that the about page shows a testimonial if
        there is one in the database
        '''
        test_user = User.objects.create(
            username='adhatton',
            password='adam',
        )
        testimonial = Testimonial.objects.create(
            user=test_user,
            content='test testimonial',
            approved=True
        )
        testimonial_card = (
            b'<div class="card h-100 flex-row align-items-center">'
        )
        response = self.client.get('/about/')
        assert testimonial_card in response.content
