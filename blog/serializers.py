from rest_framework import serializers
from .models import Post, Comment
from main_auth.serializers import UserLessInfoSerializer 


class TypeBaseSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True, many=False)
    am_i_author = serializers.SerializerMethodField(read_only=True)
    is_liked_by_me = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_am_i_author(self,obj):
        current_user = self.context.get('request').user
        return True if current_user == obj.author else False

    def get_likes(self,obj):
        return obj.likes.count()

    def get_is_liked_by_me(self,obj):
        current_user = self.context.get('request').user
        return True if current_user in obj.likes.all() else False
    
    class Meta:
        abstract = True


class CommentSerializer(TypeBaseSerializer):
    class Meta: 
        model = Comment
        fields = '__all__'
     
  

class PostSerializer(TypeBaseSerializer):
    most_popular_comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields ='__all__'

    def get_most_popular_comment(self, obj):
        if obj.post_comments.all().count()>0:
            comment = obj.post_comments.all().first()
            return CommentSerializer(comment, many=False, 
            context={'request':self.context.get('request')}).data
        else:
            return False

   
class PostDetailSerializer(TypeBaseSerializer):
    post_comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields ='__all__'


