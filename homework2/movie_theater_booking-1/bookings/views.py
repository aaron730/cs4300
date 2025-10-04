from django.shortcuts import render
from django.http import HttpResponse
from .models import Booking

def index(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings/index.html', {'bookings': bookings})

def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'bookings/detail.html', {'booking': booking})

def create_booking(request):
    if request.method == 'POST':
        # Logic to create a booking
        pass
    return render(request, 'bookings/create.html')

def update_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        # Logic to update the booking
        pass
    return render(request, 'bookings/update.html', {'booking': booking})

def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return HttpResponse('Booking deleted successfully.')
    return render(request, 'bookings/delete.html', {'booking': booking})