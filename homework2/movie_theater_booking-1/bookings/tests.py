from django.test import TestCase
from .models import Booking

class BookingModelTest(TestCase):

    def setUp(self):
        self.booking = Booking.objects.create(
            movie_title="Inception",
            show_time="2023-10-01 20:00",
            seats=2
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.movie_title, "Inception")
        self.assertEqual(self.booking.seats, 2)

    def test_booking_str(self):
        self.assertEqual(str(self.booking), "Inception - 2 seats")