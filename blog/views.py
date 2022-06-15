from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Response, status
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions  import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import exceptions
from main_auth.models import User
from .permissions import IsAuthorOrReadOnly
from core.pagination import MyPagination

from rest_framework.decorators import api_view, permission_classes
# Create your views here.
class PostsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()
    
    def get(self, request):
        posts = self.get_queryset()
        serializer = PostSerializer(posts, many=True,context={'request':request})
        paginator = MyPagination()
        page = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(page)
    
    def post(self, request):
        data = request.data 
        if not data.get('body') or not data.get("title"):
            raise exceptions.APIException("Body or title cannot be blank!")
        if(len(data.get('body'))<1 or len(data.get('title')) <1):
            raise exceptions.APIException("Body or title cannot be blank!")

        post = Post(
            body=data.get('body'),
            author=request.user,
            title=data.get("title")
        )
        post.save()
        serializer = PostSerializer(post,context={'request':request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    
class PostView(APIView):
    permission_classes = (IsAuthorOrReadOnly, )

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def delete(self, request, pk):
        print(request.user)
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response("Deleted", status=status.HTTP_200_OK)


class UserPostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, username):
        user = User.objects.all().get(username=username)
        return Post.objects.all().filter(author=user)
    
    def get(self, request,username):
        posts =self.get_queryset(username)
        serializer = PostSerializer(posts, many=True,context={'request':request})
        return Response(serializer.data)
    

@api_view(["PATCH"])
@permission_classes((IsAuthenticated,),)
def like_dislike_post(request):
    post_id = request.data.get("id")
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    post.save()
    serializer = PostSerializer(post, many=False,context={'request':request})
    return Response(serializer.data, status=status.HTTP_200_OK)