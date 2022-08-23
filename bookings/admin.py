from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Adds Booking model into the admin site
    """

    list_display = ("date", "time", "type", "user", "created_on", "updated_on")
