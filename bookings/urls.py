from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path


urlpatterns = [
    path('bookings/', login_required(views.BookingsPage.as_view()), name='bookings'),
]
