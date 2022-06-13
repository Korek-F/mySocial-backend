from rest_framework import serializers
from .models import Post
from main_auth.serializers import UserLessInfoSerializer 

class PostSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True, many=False)
    am_i_author = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    is_liked_by_me = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields ='__all__'

    def get_am_i_author(self,obj):
        current_user = self.context.get('request').user
        return True if current_user == obj.author else False

    def get_likes(self,obj):
        return obj.likes.count()
    
    def get_is_liked_by_me(self,obj):
        current_user = self.context.get('request').user
        return True if current_user in obj.likes.all() else False