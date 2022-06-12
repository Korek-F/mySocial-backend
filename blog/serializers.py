from rest_framework import serializers
from .models import Post
from main_auth.serializers import UserLessInfoSerializer 

class PostSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True, many=False)
    am_i_author = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields ='__all__'

    def get_am_i_author(self,obj):
        current_user = self.context.get('request').user
        return True if current_user == obj.author else False
