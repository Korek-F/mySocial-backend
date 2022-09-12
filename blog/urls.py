from . import views
from django.urls import path



urlpatterns = [
    path("posts", views.PostsView.as_view(), name="posts"),
    path("post-delete/<int:pk>", views.PostView.as_view(), name="posts_delete"),
    path("user/<str:username>", views.UserPostView.as_view(), name="user_posts"),
    path("post/like-dislike", views.like_dislike_post, name="post_like_dislike"),
    path("post/<int:pk>/", views.PostView.as_view(), name="post_details"),
    path("post/<int:id>/details", views.CommentsView.as_view(), name="post_comments"),
    path("comment/like-dislike", views.like_dislike_comment, name="comment_like_dislike"),
    path("comment/<int:pk>/", views.CommentView.as_view(), name="comment"),
    path("comment-delete/<int:pk>", views.CommentView.as_view(), name="comment_delete"),
    path("notifications", views.notifications, name="notifications"),
     path("seen-notifications", views.seen_notifications, name="seen_notifications"),
     path("unseen-notifications-count", views.unseen_notifications_count, name="unseen_notifications_count"),
]
