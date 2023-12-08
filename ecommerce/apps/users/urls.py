from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = SimpleRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('users/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('users/login/refresh/', TokenRefreshView.as_view(), name='token-refresh')
]

urlpatterns += router.urls
