from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    '''
    Model for contact from website users
    '''

    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    completed = models.BooleanField(default=False)

    class Meta:
        '''
        Sets metadata for the Contact class
        '''

        ordering = ['-submitted']

    def __str__(self):
        return (
            f'Contact from {self.name} on '
            f'{self.submitted.strftime("%d %b %Y")}'
        )
