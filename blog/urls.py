from . import views
from django.urls import path



urlpatterns = [
    path("all-posts", views.PostView.as_view())
]
