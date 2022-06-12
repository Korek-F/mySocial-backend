from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Response, status
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions  import IsAuthenticatedOrReadOnly
from rest_framework import exceptions
from main_auth.models import User
from .permissions import IsAuthorOrReadOnly
# Create your views here.
class PostsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()
    
    def get(self, request):
        posts = self.get_queryset()
        serializer = PostSerializer(posts, many=True,context={'request':request})
        return Response(serializer.data)
    
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
    