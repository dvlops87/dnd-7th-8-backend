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
    path('info/', views.mypage),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)