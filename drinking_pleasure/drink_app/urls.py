from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('get/list/',views.DrinkGetList.as_view()),
    path('get/<int:pk>',views.DrinkDetail.as_view()),
    path('review/<int:pk>',views.DrinkReview.as_view()),
    path('like/<int:pk>',views.DrinkLike.as_view()),
    path('like/comment/<int:pk>',views.DrinkCommentLike.as_view()),
]