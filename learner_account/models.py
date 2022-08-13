from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class LearnerProfile(models.Model):
    '''
    Model to extend user and include additional learner information
    '''
    ABILITY_CHOICES = [('','Choose your level'),('B', 'Beginner'),('I','Intermediate'),('A', 'Advanced')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)
    ability = models.CharField(max_length=1,choices=ABILITY_CHOICES)
    about = models.TextField(blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'