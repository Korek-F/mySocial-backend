from asyncio import constants
from enum import auto
from multiprocessing import context
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Response, status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
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
    permission_classes = (IsAuthorOrReadOnly,)

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request,pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response("Deleted", status=status.HTTP_200_OK)


class CommentsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_queryset(self, id):
        return Post.objects.get(pk=id).post_comments.all().filter(parent__isnull=True)

    def get(self, request, id):
        post = self.get_queryset(id)
        serialzer =  CommentSerializer(post, many=True, context={'request':request})
        return Response(serialzer.data)
    
    def post(self, request, id):
        user = request.user 
        post = get_object_or_404(Post, pk=id)
        content = request.data.get("content")
        parent_id = request.data.get("parent_id")
        comment = Comment(author=user, post=post,content=content)
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            comment.parent = parent_comment
        comment.save()
        serialzer =  CommentSerializer(comment, many=False, context={'request':request})
        return Response(serialzer.data, status=status.HTTP_201_CREATED)
    
class CommentView(APIView):
    permission_classes = (IsAuthorOrReadOnly,)

    def get_object(self,pk):
        return get_object_or_404(Comment, pk=pk)
    
    def get(self, request,pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        comment = self.get_object(pk)
        self.check_object_permissions(request, comment)
        comment.delete()
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

@api_view(["PATCH"])
@permission_classes((IsAuthenticated,),)
def like_dislike_comment(request):
    comment_id = request.data.get("id")
    user = request.user 
    comment = get_object_or_404(Comment, pk=comment_id)
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    comment.save() 
    serializer = CommentSerializer(comment, many=False, context={'request':request})
    return Response(serializer.data, status=status.HTTP_200_OK)