
from datetime import timedelta
from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    def ready(self):
        from bookings.models import Movie, Seat
        # Insert a movie if it doesn't exist
        Movie.objects.get_or_create(
            title='Sample Movie',
            defaults={
                'description': 'A sample movie for demo purposes.',
                'release_date': '2025-01-01',
                'duration': timedelta(hours=2),
            }
        )
        Movie.objects.get_or_create(
            title='The Great Adventure',
            defaults={
                'description': 'An epic journey across uncharted lands.',
                'release_date': '2024-12-15',
                'duration': timedelta(hours=2, minutes=15),
            }
        )
        Movie.objects.get_or_create(
            title='Comedy Night',
            defaults={
                'description': 'A hilarious night of stand-up comedy.',
                'release_date': '2025-02-10',
                'duration': timedelta(hours=1, minutes=45),
            }
        )
        Movie.objects.get_or_create(
            title='Space Odyssey',
            defaults={
                'description': 'A sci-fi adventure beyond the stars.',
                'release_date': '2025-03-20',
                'duration': timedelta(hours=2, minutes=30),
            }
        )
        # Insert a few seats if they don't exist
        for seat_num in ['A1', 'A2', 'A3']:
            Seat.objects.get_or_create(seat_number=seat_num)
