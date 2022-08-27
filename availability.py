import datetime
from bookings.models import Booking


def get_booking_availability():
    '''
    Creates a dictionary with the availability of the next 7 days
    to use with the context of the Booking view
    '''
    LESSON_SLOTS = {
        '10': '10:00 - 11:00',
        '11': '11:00 - 12:00',
        '13': '13:00 - 14:00',
        '14': '14:00 - 15:00',
        '15': '15:00 - 16:00',
        '16': '16:00 - 17:00',
    }
    bookings_queryset = Booking.objects.all()
    today = datetime.date.today()
    next_7_days = get_next_7_days(today)
    lesson_availablility = {}

    for day_index, day in enumerate(next_7_days):
        lesson_availablility[f'day_{day_index + 1}'] = day
        for slot_index, (slot_k, slot_v) in enumerate(LESSON_SLOTS.items()):
            if bookings_queryset.filter(date=day).filter(time=slot_k).exists():
                lesson_availablility[
                    f'day_{day_index + 1}_slot_{slot_index + 1}'
                ] = 'BOOKED'
            else:
                lesson_availablility[
                    f'day_{day_index + 1}_slot_{slot_index + 1}'
                ] = slot_v

    return lesson_availablility


def get_next_7_days(date):
    '''
    Returns a list of the next 7 days not including today
    '''
    days_list = []

    for num in range(7):
        date = date + datetime.timedelta(days=1)
        days_list.append(date)

    return days_list
