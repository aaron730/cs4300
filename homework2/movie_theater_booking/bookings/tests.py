from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APIClient

from .models import Movie, Seat, Booking


class ModelsTestCase(TestCase):
    """Unit tests for the models' basic behavior and string representations."""

    def setUp(self):
        """Create a movie, a seat and a test user for model tests."""
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Desc',
            release_date=timezone.now().date(),
            duration=timedelta(hours=1, minutes=30),
        )
        self.seat = Seat.objects.create(seat_number='A1')
        self.user = User.objects.create_user(username='alice', password='pass')

    def test_movie_str(self):
        """Movie.__str__ should return the movie title."""
        self.assertEqual(str(self.movie), 'Test Movie')

    def test_seat_str_and_default(self):
        """Seat.__str__ should return seat number and is_booked default is False."""
        self.assertEqual(str(self.seat), 'A1')
        self.assertFalse(self.seat.is_booked)

    def test_booking_str_and_creation(self):
        """Creating a Booking should produce a readable __str__ containing user, movie and seat."""
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertIn(self.user.username, str(booking))
        self.assertIn(self.movie.title, str(booking))
        self.assertIn(self.seat.seat_number, str(booking))


class ViewsIntegrationTestCase(TestCase):
    """Integration tests for view endpoints and end-to-end booking behavior."""

    def setUp(self):
        """Prepare a movie, some seats and a user for view tests."""
        self.client = Client()
        self.movie = Movie.objects.create(
            title='Integration Movie',
            description='Desc',
            release_date=timezone.now().date(),
            duration=timedelta(hours=2),
        )
        # create a few seats
        self.seat1 = Seat.objects.create(seat_number='B1')
        self.seat2 = Seat.objects.create(seat_number='B2')
        self.user = User.objects.create_user(username='bob', password='secret')

    def test_movie_list_view_shows_movies(self):
        """The movie list view should return HTTP 200 and include movie titles."""
        url = reverse('movie_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Integration Movie')

    def test_seat_booking_anonymous_creates_fallback_user(self):
        """Posting a booking while anonymous should mark seat booked and use fallback user."""
        url = reverse('seat_booking', args=[self.movie.id])
        resp = self.client.post(url, {'seat': self.seat1.id}, follow=True)
        self.seat1.refresh_from_db()
        self.assertTrue(self.seat1.is_booked)
        fallback = User.objects.get(username='JohnMovie')
        bookings = Booking.objects.filter(user=fallback, seat=self.seat1, movie=self.movie)
        self.assertEqual(bookings.count(), 1)

    def test_seat_booking_logged_in_user_gets_assigned(self):
        """Logged-in users should have bookings associated with their account."""
        self.client.force_login(self.user)
        url = reverse('seat_booking', args=[self.movie.id])
        resp = self.client.post(url, {'seat': self.seat2.id}, follow=True)
        self.seat2.refresh_from_db()
        self.assertTrue(self.seat2.is_booked)
        booking = Booking.objects.get(seat=self.seat2)
        self.assertEqual(booking.user, self.user)

    def test_double_booking_prevented(self):
        """Attempting to book an already-booked seat should not create a second booking."""
        url = reverse('seat_booking', args=[self.movie.id])
        self.client.post(url, {'seat': self.seat1.id}, follow=True)
        self.seat1.refresh_from_db()
        self.assertTrue(self.seat1.is_booked)

        before_count = Booking.objects.filter(seat=self.seat1).count()
        self.client.post(url, {'seat': self.seat1.id}, follow=True)
        after_count = Booking.objects.filter(seat=self.seat1).count()
        self.assertEqual(before_count, after_count)

    def test_booking_history_shows_user_bookings(self):
        """Booking history view should list bookings for the authenticated user."""
        booking = Booking.objects.create(movie=self.movie, seat=self.seat2, user=self.user)
        self.client.force_login(self.user)
        url = reverse('booking_history')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.movie.title)


class APITestCase(TestCase):
    """API endpoint tests for movie listing and booking creation."""

    def setUp(self):
        """Create API client, movie, seat and user for REST tests."""
        self.api = APIClient()
        self.movie = Movie.objects.create(
            title='API Movie',
            description='Desc',
            release_date=timezone.now().date(),
            duration=timedelta(minutes=95),
        )
        self.seat = Seat.objects.create(seat_number='C1')
        self.user = User.objects.create_user(username='carol', password='pw')

    def test_api_movie_list(self):
        """GET /api/movies/ should return a list including created movies."""
        resp = self.api.get('/api/movies/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        titles = [m.get('title') for m in data]
        self.assertIn('API Movie', titles)

    def test_api_booking_requires_auth(self):
        """Unauthenticated POST to bookings API should be rejected (401/403)."""
        resp = self.api.post('/api/bookings/', {'movie': self.movie.id, 'seat': self.seat.id})
        self.assertIn(resp.status_code, (401, 403))

    def test_api_create_booking_authenticated(self):
        """Authenticated API users should be able to create bookings via POST."""
        self.api.force_authenticate(user=self.user)
        resp = self.api.post('/api/bookings/', {'movie': self.movie.id, 'seat': self.seat.id})
        self.assertIn(resp.status_code, (200, 201))
        booking = Booking.objects.get(seat=self.seat)
        self.assertEqual(booking.user, self.user)

