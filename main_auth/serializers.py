from dataclasses import field
from rest_framework import serializers
from .models import User

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","username","password"]
        extra_kwargs = {'password':{'write_only':True}}

class UserLessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "avatar"]

class UserSerializer(serializers.ModelSerializer):
    is_followed_by_me = serializers.SerializerMethodField(read_only=True)
    followers =  serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=  User
        fields = ("id","followers","following","is_followed_by_me","username","email","created_at","avatar","cover")
        extra_kwargs = {'password': {'write_only': True}}

    def get_followers(self, obj):
        return obj.followed.count()
    
    def get_following(self, obj):
        return obj.following.count()
    
    def get_is_followed_by_me(self,obj):
        current_user = self.context.get('request').user
        print(current_user)

        return True if current_user in obj.followed.all() else False
