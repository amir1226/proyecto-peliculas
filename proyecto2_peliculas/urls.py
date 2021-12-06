"""proyecto2_peliculas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from movies import views as movies_views
from reviews import views as reviews_views

router = routers.SimpleRouter()
router.register(r'reviews', reviews_views.ReviewsViewSet)
router.register(r'movies', movies_views.MoviesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('login/', movies_views.login),
    path('', movies_views.movies_list),
    path('movies/<int:id>/', movies_views.show_movie_page),
    path('api/', include((router.urls, 'api'))),
]