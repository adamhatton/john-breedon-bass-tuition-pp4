from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


class BookingsPage(View):
    '''
    Renders the bookings page
    '''
    def get(self, request):
        '''
        Handles GET requests by rendering the bookings page
        '''
        booking_form = BookingForm(initial={'phone':request.user.learnerprofile.phone})

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
        booking_form = BookingForm(request.POST)
        booking_form.instance.user = request.user

        date = request.POST['date']
        time = request.POST['time']

        # Check if booking already exists
        if Booking.objects.filter(date=date).filter(time=time).exists():
            messages.error(request, 'That slot is unavailable, please select a different time')
            return redirect('/bookings/')

        elif booking_form.is_valid():
            booking_form.save()
            messages.success(request, 'Your lesson is booked!')
            return redirect('/bookings/')

        return render(
            request,
            'bookings.html',
            {
                'booking_form': booking_form,
            }
        )