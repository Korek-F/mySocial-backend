from . import views
from django.urls import path



urlpatterns = [
    path("posts", views.PostsView.as_view()),
    path("post/<int:pk>", views.PostView.as_view()),
    path("user/<str:username>", views.UserPostView.as_view()),
]
