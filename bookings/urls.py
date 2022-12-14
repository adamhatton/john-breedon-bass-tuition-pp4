from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path(
        'bookings/',
        login_required(views.BookingsPage.as_view()),
        name='bookings'
    ),
    path(
        'bookings/edit_booking/<booking_id>/',
        login_required(views.EditBooking.as_view()),
        name='edit_booking',
    ),
    path(
        'bookings/delete_booking/<booking_id>/',
        views.delete_booking,
        name='delete_booking',
    ),
]
