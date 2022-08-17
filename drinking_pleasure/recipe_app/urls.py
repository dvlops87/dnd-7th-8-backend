from django.urls import path
from .views import RecipeDetailView, RecipeReviewView


urlpatterns = [
    path('/detail', RecipeDetailView.as_view()),
    path('/detail/<int:pk>', RecipeDetailView.as_view()),
    path('/review/<int:pk>', RecipeReviewView.as_view()),
]
