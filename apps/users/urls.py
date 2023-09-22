from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import AuthViewSet, LoginView, LogoutView, RegisterView

router = DefaultRouter()
router.register('auth', AuthViewSet, 'auth')

urlpatterns = [
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='auth_register'),
    # path('update/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path('', include(router.urls)),
]
