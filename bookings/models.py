from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Booking(models.Model):
    '''
    Model to store lesson bookings made by learners
    '''
    LESSON_TYPE_CHOICES = [
        ('','Pick a lesson type'),
        ('H', 'Home visit'),
        ('O', 'Online'),
        ('S', 'At the Studio')
    ]
    LESSON_TIME_CHOICES = [
        ('','Pick a time slot'),
        ('10', '10:00 - 11:00'),
        ('11', '11:00 - 12:00'),
        ('13', '13:00 - 14:00'),
        ('14', '14:00 - 15:00'),
        ('15', '15:00 - 16:00'),
        ('16', '16:00 - 17:00'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    time = models.CharField(max_length=2, choices=LESSON_TIME_CHOICES)
    phone = PhoneNumberField(blank=True, help_text="Adding a phone number makes it easier for me to contact you about your lesson")
    type = models.CharField(max_length=1, choices=LESSON_TYPE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Lesson on {self.date.strftime("%a %d %B")} at {self.time}'

    class Meta:
        '''
        Sets metadata for the Booking class
        '''
        ordering = ['-date']