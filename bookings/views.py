from django.shortcuts import render
from django.views import View
from django.contrib import messages


class BookingsPage(View):
    '''
    Renders the bookings page
    '''
    def get(self, request):
        '''
        Handles GET requests by rendering the bookings page
        '''
               
        return render(
            request,
            'bookings.html',
            {
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