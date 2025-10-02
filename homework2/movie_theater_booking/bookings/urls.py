from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet, movie_list, booking_history, seat_booking

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', movie_list, name='movie_list'),  # Home page
    path('api/', include(router.urls)),       # API endpoints
    path('history/', booking_history, name='booking_history'),
    path('movies/<int:movie_id>/book/', seat_booking, name='seat_booking'),
]