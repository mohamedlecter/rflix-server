from django.shortcuts import render, redirect, get_object_or_404
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
    rated_movies = Rating.objects.filter(user=user).select_related('movie').order_by('movie__title')
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
        
        # Redirect to the same page to ensure the form submission isn't repeated
        return redirect('movies_page')

    context = {
        'rated_movies': rated_movies,
        'unrated_movies': unrated_movies
    }
    return render(request, 'movies.html', context)

@login_required
def delete_rating(request, movie_id):
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