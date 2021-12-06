from rest_framework.viewsets import ModelViewSet
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewsViewSet(ModelViewSet):
    queryset = Review.objects
    serializer_class = ReviewSerializer
