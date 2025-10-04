from django.contrib import admin
from .models import Booking, Movie, Theater

admin.site.register(Booking)
admin.site.register(Movie)
admin.site.register(Theater)