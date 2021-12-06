from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from movies.models import Movie


class Review(models.Model):
    titulo=models.CharField(max_length=100)
    comentario=models.TextField(max_length=1000)
    fecha=models.DateField(auto_now_add=True)
    estrellas = models.DecimalField(decimal_places=1, max_digits=2)

    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo