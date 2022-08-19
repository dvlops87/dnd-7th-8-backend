from django.urls import path
from .views import RecipeDetailView, RecipeReviewView, RecipeLikeView,\
     RecipeView, MeterialView


urlpatterns = [
    path('', RecipeView.as_view()),
    path('detail', RecipeDetailView.as_view()),
    path('detail/<int:pk>', RecipeDetailView.as_view()),
    path('review/<int:pk>', RecipeReviewView.as_view()),
    path('like/<int:recipe_id>', RecipeLikeView.as_view()),
    path('meterial', MeterialView.as_view()),
]
