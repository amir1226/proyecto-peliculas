import requests
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from movies.models import Movie
from movies.serializers import MovieSerializer


def login(request):
    return render(request, "login_register.html")


def movies_list(request):
    movies = Movie.objects.all()

    return render(request, 'movies_list.html',
                  context={
                      "movies": movies,
                      "usuario": str(request.user)
                  })


def show_movie_page(request, id):
    if request.method == "GET":
        movie = requests.get(f'http://localhost:8000/api/movies/{id}/')
        return render(request, 'movie.html',
                      context={
                          "movie": movie.json(),
                          "usuario": str(request.user)
                      })


class MoviesViewSet(ModelViewSet):
    queryset = Movie.objects
    serializer_class = MovieSerializer
    # http_method_names = ['get', 'post']
