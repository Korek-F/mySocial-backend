from . import views
from django.urls import path



urlpatterns = [
    path("posts", views.PostsView.as_view()),
    path("post-delete/<int:pk>", views.PostView.as_view()),
    path("user/<str:username>", views.UserPostView.as_view()),
    path("post/like-dislike", views.like_dislike_post),
    path("post/<int:pk>/", views.PostView.as_view()),
    path("post/<int:id>/details", views.CommentsView.as_view()),
    path("comment/like-dislike", views.like_dislike_comment),
]
