from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=150)
    year = models.IntegerField(validators=[MinValueValidator(1900),
                                           MaxValueValidator(2200)],
                               default=timezone.datetime.now().year)
    rating = models.DecimalField(max_digits=4, decimal_places=3,
                                 validators=[MinValueValidator(0.000),
                                             MaxValueValidator(5.000)],
                                 default=0.000)
    nratings = models.PositiveIntegerField(default=0)

    # Method to update the global rating of the movie
    def update_global_rating(self, new_rating=None, old_rating=None): 
        if old_rating is not None:  # If the user has already rated the movie
            self.rating = (self.rating * self.nratings + (new_rating - old_rating)) / self.nratings  # Update rating
        else:  # If the user is rating the movie for the first time
            self.nratings += 1  # Increment the number of ratings
            self.rating = (self.rating * (self.nratings - 1) + new_rating) / self.nratings  # Update rating
        self.save()

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personal_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}: {self.personal_rating}"
class MovieParty(models.Model):
    name = models.CharField(max_length=150, unique=True) 
    members = models.ManyToManyField(User, related_name="movie_parties", blank=True)

    def is_full(self):
        """Checks if the party has reached its maximum capacity of 10 members."""
        return self.members.count() >= 10

    def member_count(self):
        """Returns the current number of members in the party."""
        return self.members.count()

    def __str__(self):
        """String representation of the MovieParty object."""
        return self.name