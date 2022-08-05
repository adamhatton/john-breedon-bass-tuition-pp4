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

    def post(self, request, *args, **kwargs):
        '''
        Handles POST requests from the contact form on the home page
        '''
        contact_form = ContactForm(data=request.POST)

        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.save()

        return render(
            request,
            'index.html',
            {
                'contact_form': contact_form
            },
        )

class ContactSection(View):
    '''
    Replicates the HomePage view, but allows browser to scroll
    to Contact Form through JavaScript using the url
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

    def post(self, request, *args, **kwargs):
        '''
        Handles POST requests from the contact form on the home page
        '''
        contact_form = ContactForm(data=request.POST)

        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.save()

        return render(
            request,
            'index.html',
            {
                'contact_form': contact_form
            },
        )