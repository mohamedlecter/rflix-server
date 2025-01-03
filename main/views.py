from django.shortcuts import render
from main.models import Movie


def index(request):
    return render(request, 'index.html')


def movies(request):
    movies = Movie.objects.all()[:10]
    context = {'movies': movies}
    return render(request, 'movies.html', context)
