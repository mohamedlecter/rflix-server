from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title    = models.CharField(max_length=150)
    year     = models.IntegerField(validators=[MinValueValidator(1900),
                                               MaxValueValidator(2200)],
                                   default=timezone.datetime.now().year)
    rating   = models.DecimalField(max_digits=4, decimal_places=3,
                                   validators=[MinValueValidator(0.000),
                                               MaxValueValidator(5.000)],
                                   default=0.000)
    nratings = models.PositiveIntegerField(default=0)

    # update_global_rating: Update the global rating of the movie
    def update_global_rating(self, new_rating=None, old_rating=None): 
        if old_rating is not None: # If the user has already rated the movie
            self.rating = (self.rating * self.nratings + (new_rating - old_rating)) / self.nratings # Update the rating
        else: # If the user has not rated the movie before
            self.nratings += 1 # Increment the number of ratings
            self.rating = (self.rating * (self.nratings - 1) + new_rating) / self.nratings # Update the rating
        self.save()

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    personal_rating  = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    date    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}: {self.personal_rating}"
