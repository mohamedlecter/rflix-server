"""rflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('movies/', views.movies_page, name='movies_page'),
    path('movies/delete-rating/<int:movie_id>/', views.delete_rating, name='delete_rating'),
    path("profile/", views.profile, name="profile"),
    path("recommendations/", views.recommendations, name="recommendations"),
    path("movie-parties/", views.parties, name="parties"),
    path("movie-parties/create/", views.create_movie_party, name="create_movie_party"),
    path('movie-parties/<int:party_id>/recommendations/', views.movie_party_recommendations, name='movie_party_recommendations'),
    path('reporting_page/', views.reporting_page, name='reporting_page'),
    ]

