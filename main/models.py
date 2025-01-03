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

