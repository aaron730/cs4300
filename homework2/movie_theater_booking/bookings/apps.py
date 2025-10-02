from datetime import timedelta
import sys
from django.apps import AppConfig
from django.db.utils import OperationalError


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    def ready(self):
        # Avoid touching the database while running management commands that
        # create/alter the database schema or run tests.
        if len(sys.argv) > 1 and sys.argv[1] in (
            'makemigrations', 'migrate', 'collectstatic', 'test',
        ):
            return

        try:
            from bookings.models import Movie, Seat

            # Seed a few example movies (safe no-op if they already exist)
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

            # Seed a few seats
            for seat_num in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
                             'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
                            'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                            'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10']:
                Seat.objects.get_or_create(seat_number=seat_num)

        except OperationalError:
            # DB isn't ready yet (e.g. during initial migrate); skip seeding
            pass
