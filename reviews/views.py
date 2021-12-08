import requests
from django.shortcuts import render, redirect
from django.middleware import csrf
from datetime import datetime

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewsViewSet(ModelViewSet):
    queryset = Review.objects
    serializer_class = ReviewSerializer


def edit_review(request, id):
    if request.method == "POST":
        title = request.POST["title"]
        review_text = request.POST["review"]
        score = request.POST["score"]
        movie = request.POST["movie"]
        csrf_token = csrf.get_token(request)
        payload = {"titulo": title, "comentario": review_text, "estrellas": score,"movie":movie}
        cookies = {'csrftoken': csrf_token, 'sessionid': request.session.session_key}
        response = requests.put(f'http://127.0.0.1:8000/api/reviews/{id}/', cookies=cookies,
                                json=payload)
        return redirect(f'/movies/{movie}') if response.status_code == status.HTTP_200_OK else \
            render(request, "error.html", context={"status": response.status_code, "error": response.json()})

    review = requests.get(f'http://127.0.0.1:8000/api/reviews/{id}/')
    review_json = review.json()
    if request.user.username == review_json["user"]:
        return render(request, 'review-edit.html',
                      context={
                          "review": review.json(),
                          "user": str(request.user)
                      })
    return redirect(f'/movies/{review_json["movie"]}')
