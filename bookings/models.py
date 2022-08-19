from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Booking(models.Model):
    '''
    Model to store lesson bookings made by learners
    '''
    LESSON_TYPE_CHOICES = [('H', 'Home visit'), ('O', 'Online'), ('S', 'At the Studio')]
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()
    phone = PhoneNumberField(blank=True, help_text="Adding a phone number makes it easier for me to contact you about your lesson")
    type = models.CharField(max_length=1, choices=LESSON_TYPE_CHOICES, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Lesson on {self.date} at {self.time}'

    class Meta:
        '''
        Sets metadata for the Booking class
        '''
        ordering = ['date']