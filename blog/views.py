from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from rest_framework.views import APIView, Response, status
from rest_framework.permissions  import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import exceptions

from .models import Post, Comment, Notification
from .serializers import NotificationSerializer, PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from main_auth.models import User
from core.pagination import MyPagination



class PostsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, request):
        return Post.objects.all()
        
    
    def get(self, request):
        posts = self.get_queryset(request)
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
        comment = Comment.objects.create(author=user, post=post,content=content)
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            comment.parent = parent_comment
            comment.save()
            if parent_comment.author != request.user:
                Notification.objects.get_or_create(notification_type="CR", post=comment.post, comment=comment, to_user=parent_comment.author, from_user=request.user)
        else:
            if post.author != request.user:
                Notification.objects.get_or_create(notification_type="C", post=comment.post, comment=comment, to_user=post.author, from_user=request.user)
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


@api_view(["GET"])
@permission_classes((IsAuthenticated,),)
def notifications(request):
    user_notifications = Notification.objects.filter(to_user=request.user)[:40]
    serializer = NotificationSerializer(user_notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes((IsAuthenticated,),)
def unseen_notifications_count(request):
    user_notifications = Notification.objects.filter(has_been_seen=False, to_user=request.user).count()
    return Response(user_notifications, status=status.HTTP_200_OK)

        
@api_view(["GET"])
@permission_classes((IsAuthenticated,),)
def seen_notifications(request):
    user_notifications = Notification.objects.filter(to_user=request.user)
    unseen_notifications = user_notifications.filter(has_been_seen=False)
    for n in unseen_notifications:
        n.has_been_seen = True
        n.save()
    return Response("OK", status=status.HTTP_200_OK)

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
        if request.user != post.author:
            Notification.objects.get_or_create(notification_type="L",
            post=post, to_user=post.author, from_user=request.user)
    post.save()
    serializer = PostSerializer(post, many=False,context={'request':request})
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

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
        if request.user != comment.author:
            Notification.objects.get_or_create(notification_type="LC", post=comment.post, comment=comment, to_user=comment.author, from_user=request.user)
    comment.save() 
    serializer = CommentSerializer(comment, many=False, context={'request':request})
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)