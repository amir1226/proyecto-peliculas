import requests
from django.contrib.auth import authenticate, login
from django.middleware import csrf
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from movies.models import Movie
from movies.serializers import MovieSerializer
from reviews.models import Review


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if(user is not None):
            login(request, user)
            return redirect('/')
        return render(request, "error.html", context={"error": "Authentication failed"})

    return render(request, "login_register.html", context={
        "user": str(request.user)
    })


def movies_list(request):
    api_url = f'http://127.0.0.1:8000/api/movies'
    search=""
    if request.method == "POST":
        search = request.POST["movie-searcher"]
        api_url += f'?search={search}' if search else '/'

    movies = requests.get(api_url)
    return render(request, 'movies_list.html',
                  context={
                      "movies": movies.json(),
                      "user": str(request.user),
                      "search_value": search
                  })


def show_movie_page(request, id):
    if request.method == "POST":
        title = request.POST["title"]
        review_text = request.POST["review"]
        score = request.POST["score"]
        user = request.user
        movie = Movie.objects.get(id=id)
        new_review = Review.objects.create(titulo=title, comentario=review_text, estrellas=score,
                                           movie=movie, user=user)
        new_review.save()
        return redirect(f'/movies/{id}/')
    movie = requests.get(f'http://127.0.0.1:8000/api/movies/{id}/')
    return render(request, 'movie.html',
                  context={
                      "movie": movie.json(),
                      "user": str(request.user)
                  })


def register(request):
    if (request.method == "POST"):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        payload = {"username":username, "email":email, "password1":password,"password2":confirm_password}
        cookies = {'csrftoken': csrf.get_token(request)}
        response = requests.post('http://127.0.0.1:8000/api/rest-auth/registration/', cookies=cookies,
                                 json=payload)
        if response.status_code == status.HTTP_201_CREATED:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, "error.html", context={"status": response.status_code, "error": response.json()})

    return redirect('/login/')

def logout(request):
    if request.method == 'POST':
        if request.user != "AnonymousUser":
            csrf_token = csrf.get_token(request)
            cookies = {'csrftoken': csrf_token, 'sessionid': request.session.session_key}
            response = requests.post('http://127.0.0.1:8000/api/rest-auth/logout/', cookies=cookies)
            return redirect('/') if response.status_code == status.HTTP_200_OK else \
                render(request, "error.html", context={"status": response.status_code, "error": response.json()})

    return redirect('/login/')


class MoviesViewSet(ModelViewSet):
    queryset = Movie.objects
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = Movie.objects.filter(titulo__contains=search)
        return queryset