from django.db import models

# Create your models here.
class Director(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Movie(models.Model):
    titulo=models.CharField(max_length=100)
    genero=models.CharField(max_length=50)
    fecha_publicacion = models.DateField()
    imagen = models.CharField(null=True, max_length=400)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return f"Movie: {self.titulo}"