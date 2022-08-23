import random
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from learner_account.models import Testimonial
from .forms import ContactForm


def index_page(request):
    """
    Loading index redirects to the homepage
    """
    return HttpResponseRedirect("/home/")


class HomePage(View):
    """
    Renders the homepage and handles the contact form
    """

    def get(self, request):
        """
        Handles GET requests by rendering the homepage and contact form
        """
        return render(
            request,
            "home.html",
            {"contact_form": ContactForm()},
        )


class ContactSection(View):
    """
    Replicates the HomePage view, but allows browser to scroll
    to Contact Form through JavaScript using the url
    """

    def get(self, request):
        """
        Handles GET requests by rendering the homepage and contact form
        """
        return render(
            request,
            "home.html",
            {"contact_form": ContactForm()},
        )

    def post(self, request):
        """
        Handles POST requests from the contact form on the home page
        """
        contact_form = ContactForm(data=request.POST)

        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.save()
            messages.success(request, "Message sent successfully")
            contact_form = ContactForm()

        return render(
            request,
            "home.html",
            {"contact_form": contact_form},
        )


def about_page(request):
    """
    View for loading the about page
    """
    queryset = Testimonial.objects.filter(approved=True)
    testimonial_pks = [i.pk for i in queryset]
    random.shuffle(testimonial_pks)
    random_testimonials = [queryset.get(id=i) for i in testimonial_pks]

    return render(
        request,
        "about.html",
        {"testimonials": random_testimonials},
    )
