from django.test import TestCase
from django.contrib.auth.models import User
from .models import LearnerProfile, Testimonial


class TestLearnerProfileModel(TestCase):
    '''Class for testing the LearnerProfile Model'''

    def setUp(self):
        '''
        Create a user object to use in all tests. Creating
        the user will also create the LearnerProfile
        '''
        User.objects.create(
            username='adhatton',
            password='password',
        )

    def test_ability_max_length(self):
        '''Test that ability field has max length of 1'''
        test_user = User.objects.get(pk=1)
        profile = LearnerProfile.objects.get(user=test_user)
        max_length = profile._meta.get_field('ability').max_length
        self.assertEqual(max_length, 1)

    def test_learner_profile_str_method(self):
        '''Test the string method returns expected string'''
        test_user = User.objects.get(pk=1)
        profile = LearnerProfile.objects.get(user=test_user)
        expected_string = 'Profile for adhatton'
        self.assertEqual(str(profile), expected_string)

    def test_create_user_creates_learner_profile(self):
        '''Tests that creating a user also creates a learner profile'''
        test_user = User.objects.get(pk=1)
        self.assertTrue(LearnerProfile.objects.filter(user=test_user))


class TestTestimonialModel(TestCase):
    '''Class for testing the Testimonial Model'''

    def setUp(self):
        '''
        Create a user object and Testimonial object to use in all tests
        '''
        test_user = User.objects.create(
            username='adhatton',
            password='password',
        )
        Testimonial.objects.create(user=test_user, content='test')

    def test_approved_defaults_to_false(self):
        '''Test that the approved field defaults to False'''
        test_user = User.objects.get(pk=1)
        testimonial = Testimonial.objects.get(user=test_user)
        self.assertFalse(testimonial.approved)

    def test_testimonial_str_method(self):
        '''Test the string method returns expected string'''
        test_user = User.objects.get(pk=1)
        testimonial = Testimonial.objects.get(user=test_user)
        expected_string = f'{testimonial.content}'
        self.assertEqual(str(testimonial), expected_string)
