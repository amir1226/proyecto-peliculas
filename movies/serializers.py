from rest_framework import serializers
from reviews.serializers import ReviewSerializer
from .models import Movie, Director


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    director = serializers.StringRelatedField()
    class Meta:
        model = Movie
        fields = '__all__'