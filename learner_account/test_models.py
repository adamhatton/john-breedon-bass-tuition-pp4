# from django.test import TestCase
# from .models import Contact


# class TestContactModel(TestCase):
#     '''Class for testing the Contact Model'''

#         def test_create_user_creates_learner_profile(self):
#         '''Tests that creating a user also creates a learner profile'''
#         test_user = User.objects.get(pk=1)
#         self.assertTrue(LearnerProfile.objects.filter(user=test_user))

#     def setUp(self):
#         '''Create a contact object to use in all tests'''
#         Contact.objects.create(
#             name='Adam',
#             email='test@test.co.uk',
#             phone='07450039175',
#             message='test message'
#         )

#     def test_name_max_length(self):
#         '''Test that name field has max length of 30'''
#         contact = Contact.objects.get(id=1)
#         max_length = contact._meta.get_field('name').max_length
#         self.assertEqual(max_length, 30)

#     def test_completed_defaults_to_false(self):
#         '''Test that the completed field defaults to False'''
#         contact = Contact.objects.get(id=1)
#         self.assertFalse(contact.completed)

#     def test_contact_str_method(self):
#         '''Test the string method returns expected string'''
#         contact = Contact.objects.get(id=1)
#         expected_string = (
#             f'Contact from {contact.name} on '
#             f'{contact.submitted.strftime("%d %b %Y")}'
#         )
#         self.assertEqual(str(contact), expected_string)
