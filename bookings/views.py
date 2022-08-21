from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import availability
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
        booking_form = BookingForm(initial={'phone': request.user.learnerprofile.phone})
        booking_availability = availability.get_booking_availability()

        return render(
            request,
            'bookings.html',
            {
                'booking_availability': booking_availability,
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


class EditBooking(View):
    '''
    Renders the bookings page with a specific instance of a booking for
    amending
    '''
    def get(self, request, booking_id):
        '''
        Finds the booking to edit and renders the bookings page
        '''
        booking_to_edit = get_object_or_404(Booking, pk=booking_id)
        booking_form = BookingForm(instance=booking_to_edit)
        booking_availability = availability.get_booking_availability()

        return render(
            request,
            'bookings.html',
            {
                'booking_availability': booking_availability,
                'booking_form': booking_form,
            }
        )

    def post(self, request, booking_id):
        '''
        Handles POST requests to the edit_bookings page
        '''
        queryset = Booking.objects.all()
        booking_to_edit = get_object_or_404(queryset, pk=booking_id)
        booking_form = BookingForm(request.POST, instance=booking_to_edit)

        date = request.POST['date']
        time = request.POST['time']

        # Check if booking already exists
        if queryset.filter(date=date).filter(time=time).exists():
            messages.error(request, 'That slot is unavailable, please select a different time')
            return redirect(f'/bookings/edit_booking/{booking_id}')

        elif booking_form.is_valid():
            booking_form.save()
            messages.success(request, 'Your lesson has been successfully changed!')
            return redirect('/learner_account/')

        booking_availability = availability.get_booking_availability()

        return render(
            request,
            'bookings.html',
            {
                'booking_availability': booking_availability,
                'booking_form': booking_form,
            }
        )

@login_required
def delete_booking(request, booking_id):
    '''
    Deletes a booking from the database
    '''
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.delete()
        messages.success(request, 'Booking successfully deleted')
    return redirect('/learner_account/')