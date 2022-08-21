from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('recipe-type/',views.RecipeType.as_view()),
    path('hot-recipe/',views.HotRecipe.as_view()),
    path('hot-review/',views.HotReview.as_view()),
]