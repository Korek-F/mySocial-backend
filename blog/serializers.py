from rest_framework import serializers
from .models import Post
from main_auth.serializers import UserLessInfoSerializer 

class PostSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True, many=False)
    class Meta:
        model = Post
        fields ='__all__'