import datetime
from bookings.models import Booking


def get_booking_availability():
    '''
    Creates a dictionary with the availability of the next 7 days
    to use with the context of the Booking view
    '''
    LESSON_SLOTS = [
        '10:00 - 11:00',
        '11:00 - 12:00',
        '13:00 - 14:00',
        '14:00 - 15:00',
        '15:00 - 16:00',
        '16:00 - 17:00',
    ]
    bookings_queryset = Booking.objects.all()
    date = datetime.date.today()
    next_7_days = get_next_7_days(date)
    lesson_availablility = {}

    for index, day in enumerate(next_7_days):
        lesson_availablility[f'day_{index + 1}'] = day
        for slot in LESSON_SLOTS:
            if bookings_queryset.filter(date=day).filter(time=slot).exists():
                lesson_availablility[f'day_{index + 1}_slot_{index + 1}'] = 'BOOKED'
            else:
                lesson_availablility[f'day_{index + 1}_slot_{index + 1}'] = slot

    return lesson_availablility


def get_next_7_days(date):
    '''
    Returns a list of the next 7 days not including today
    '''
    days_list = []

    for num in range(7):
        date = date + datetime.timedelta(days=1)
        days_list.append(num)

    return days_list
