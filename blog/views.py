from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions  import IsAuthenticatedOrReadOnly
from rest_framework import exceptions
# Create your views here.
class PostView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()
    
    def get(self, request):
        posts = self.get_queryset()
        serializer = PostSerializer(posts, many=True)
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
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    