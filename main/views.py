from django.shortcuts import render, redirect, get_object_or_404
from main.models import Movie, Rating
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RatingForm, UserLoginForm, UserRegisterForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    request.session.set_expiry(1800)
    return render(request, 'index.html')

from main.forms import RatingForm

def movies_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    request.session.set_expiry(1800)  # Refresh session expiry on activity
    user = request.user
    rated_movies = Rating.objects.filter(user=user).select_related('movie').order_by('movie__title')
    rated_movie_ids = [rating.movie.id for rating in rated_movies]
    unrated_movies = Movie.objects.exclude(id__in=rated_movie_ids).order_by('title')

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            movie_id = request.POST.get("movie_id")
            movie = Movie.objects.get(id=movie_id)
            stars = form.cleaned_data['stars']
            rating, created = Rating.objects.get_or_create(user=user, movie=movie)
            old_stars = rating.personal_rating if not created else None
            rating.personal_rating = stars
            rating.save()
            movie.update_global_rating(new_rating=stars, old_rating=old_stars)
            messages.success(request, "Rating updated successfully.")
            return redirect('movies_page')

    else:
        form = RatingForm()

    context = {
        'rated_movies': rated_movies,
        'unrated_movies': unrated_movies,
        'form': form,
    }
    return render(request, 'movies.html', context)

def delete_rating(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    movie = get_object_or_404(Movie, id=movie_id)
    rating = get_object_or_404(Rating, user=user, movie=movie)
    old_stars = rating.personal_rating
    rating.delete()  # Delete the rating
    movie.update_global_rating(new_rating=0, old_rating=old_stars)  # Update the movie's global rating
    messages.success(request, f"Your rating for '{movie.title}' has been deleted.")
    return redirect('movies_page')  # Redirect to the movies page

def login_view(request):
    
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session.set_expiry(1800)  # Set session to expire after 30 minutes of inactivity
            messages.success(request, "Logged in successfully!")
            return redirect('movies_page')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form, 'title': "Login"})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': "Register"})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    request.session.set_expiry(1800)  # Refresh session expiry on activity
    username = request.user.username
    email = request.user.email

    context = {
        'username': username,
        'email': email,
    }
    return render(request, 'profile.html', context)