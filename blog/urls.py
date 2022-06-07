from . import views
from django.urls import path



urlpatterns = [
    path("all-posts", views.PostView.as_view()),
    path("all-posts/<str:username>", views.UserPostView.as_view())
]
