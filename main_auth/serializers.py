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