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
    path('follow-action/', views.follow_action),
    path('edit-user/', views.EditUser.as_view()),
    path('delete-user/', views.DeleteUserView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
]
