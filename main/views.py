from django.shortcuts import render, redirect
from main.models import Movie, Rating
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

@login_required
def movies_page(request):
    user = request.user
    rated_movies = Rating.objects.filter(user=user).select_related('movie')
    rated_movie_ids = [rating.movie.id for rating in rated_movies]
    unrated_movies = Movie.objects.exclude(id__in=rated_movie_ids).order_by('title')

    if request.method == "POST":
        movie_id = request.POST.get("movie_id")
        stars = int(request.POST.get("stars"))
        movie = Movie.objects.get(id=movie_id)
        rating, created = Rating.objects.get_or_create(user=user, movie=movie)
        old_stars = rating.personal_rating if not created else None
        rating.personal_rating = stars
        rating.save()
        movie.update_global_rating(new_rating=stars, old_rating=old_stars)
        messages.success(request, "Rating updated successfully.")

    context = {
        'rated_movies': rated_movies,
        'unrated_movies': unrated_movies
    }
    return render(request, 'movies.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('movies_page')
        else :
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, "Account created successfully. Please log in.")
                return redirect('login')
    return render(request, 'register.html')