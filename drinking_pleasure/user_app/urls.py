from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('create/',views.signup),
    path('login/',views.login),
    path('logout/', views.logout),
    path('wdrl/', views.wdrl),
    path('update/', views.update),
    path('update/password/', views.update_password),
    path('mypage/profile/', views.MyPageProfile.as_view()),
    path('mypage/review/', views.MyPageReview.as_view()),
    path('mypage/recipe/', views.MyPageRecipe.as_view()),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)