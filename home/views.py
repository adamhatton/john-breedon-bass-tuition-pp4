from django.shortcuts import render
from django.views import View
from .forms import ContactForm


class HomePage(View):
    '''
    Renders the homepage and handles the contact form
    '''
    def get(self, request):
        '''
        Handles GET requests by rendering the homepage and contact form
        '''
        return render(
            request,
            'index.html',
            {
                'contact_form': ContactForm()
            },
        )
