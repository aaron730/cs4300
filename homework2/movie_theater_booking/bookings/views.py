from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.models import User
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
    permission_classes = [IsAuthenticatedOrReadOnly]

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        seat = self.get_object()
        # Adjust the availability logic to your models (e.g., consider showtime or movie)
        is_booked = Booking.objects.filter(seat=seat).exists()
        return Response({'seat_id': seat.pk, 'available': not is_booked})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        seat = self.get_object()
        data = {'seat': seat.pk}
        # Include extra fields if your Booking model requires them (e.g., movie/showtime)
        serializer = BookingSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(user=request.user)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().select_related('user', 'seat')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users see their own bookings only
        user = self.request.user
        return super().get_queryset().filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


