from rest_framework import viewsets
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction, IntegrityError
import logging

logger = logging.getLogger(__name__)

def movie_list(request):
    from django.conf import settings
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {
        'movies': movies,
        'PROXY_PREFIX': getattr(settings, 'PROXY_PREFIX', '')
    })


# Seat booking view
def seat_booking(request, movie_id):
    print("seat_booking view was hit")
    movie = get_object_or_404(Movie, id=movie_id)
    # load all seats so template can display booked vs available
    seats = Seat.objects.all().order_by('seat_number')
    if request.method == 'POST':
        seat = None
        seat_id = request.POST.get('seat')
        if not seat_id:
            messages.error(request, 'No seat selected. Please choose a seat to book.')
            return redirect('seat_booking', movie_id=movie_id)

        try:
            # Use a fallback username when user is anonymous or not a saved User instance
            if getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'pk', None):
                # request.user may be a SimpleLazyObject wrapping a real User
                booking_user = request.user
            else:
                booking_user, _ = User.objects.get_or_create(username='JohnMovie')

            # Use a transaction and SELECT ... FOR UPDATE to avoid double-booking under concurrency
            with transaction.atomic():
                seat = Seat.objects.select_for_update().get(id=seat_id)
                if seat.is_booked:
                    messages.error(request, 'That seat is already booked. Please choose another seat.')
                    return redirect('seat_booking', movie_id=movie_id)

                seat.is_booked = True
                seat.save()
                Booking.objects.create(movie=movie, seat=seat, user=booking_user)
        except Seat.DoesNotExist:
            messages.error(request, 'Selected seat does not exist.')
            return redirect('seat_booking', movie_id=movie_id)
        except IntegrityError:
            logger.exception('Integrity error booking seat %s for movie %s', seat_id, movie_id)
            messages.error(request, 'Could not complete booking due to a concurrent update. Please try again.')
            return redirect('seat_booking', movie_id=movie_id)
        except Exception:
            logger.exception('Failed to book seat %s for movie %s', seat_id, movie_id)
            messages.error(request, 'Could not complete booking. Please try again.')
            return redirect('seat_booking', movie_id=movie_id)
        # After booking, go to the user's booking history
        return redirect('booking_history')
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

def booking_history(request):
    # If the visitor is anonymous, show bookings for the fallback user 'JohnMovie'
    if getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'pk', None):
        target_user = request.user
    else:
        target_user, _ = User.objects.get_or_create(username='JohnMovie')

    bookings = Booking.objects.filter(user=target_user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show only bookings for the logged-in user
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the booking to the logged-in user
        serializer.save(user=self.request.user)


