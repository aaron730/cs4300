from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_email = models.EmailField()
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_tickets = models.PositiveIntegerField()

    def __str__(self):
        return f"Booking for {self.movie.title} by {self.user_email}"