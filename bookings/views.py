from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .forms import BookingForm


class BookingsPage(View):
    '''
    Renders the bookings page
    '''
    def get(self, request):
        '''
        Handles GET requests by rendering the bookings page
        '''
        booking_form = BookingForm()
               
        return render(
            request,
            'bookings.html',
            {
                'booking_form': booking_form,
            }
        )

    def post(self, request):
        '''
        Handles POST requests to the bookings page
        '''
        return render(
            request,
            'bookings.html',
            {
            }
        )