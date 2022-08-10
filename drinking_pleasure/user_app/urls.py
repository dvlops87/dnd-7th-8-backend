from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('create/',views.signup),
    path('login/',views.login),
    path('logout/', views.logout),
	path('api-jwt-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-jwt-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-jwt-auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)