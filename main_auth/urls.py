from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('registration/', views.CreateUserView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('get-user/<int:id>', views.UserDetail.as_view()),
]
