from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('registration/', views.CreateUserView.as_view()),
    path('token/', views.UserTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('get-user/<str:username>', views.UserDetail.as_view()),
    path('follow-action/', views.follow_action)
]
