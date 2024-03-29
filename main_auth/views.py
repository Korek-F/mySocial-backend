
from urllib import request
from .models import User
from .serializers import UserCreationSerializer, UserSerializer, ChangePasswordSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, permissions, views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.mail import send_mail
from django.conf import settings

from blog.models import Notification

import jwt




# Create your views here.

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_username'] = user.username
        return token


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer



class CreateUserView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(username=user_data['username'])
        token = RefreshToken.for_user(user).access_token
        absurl = 'http://'+"localhost:3000/activate/"+str(token)

        email_content = f'Hi {user.username} \n Use this link to activate your accout \n {absurl}' 

        send_mail("Verification", email_content, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):

    def post(self, request):
        token = request.data["token"]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified or not user.is_active:
                user.is_verified = True
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(views.APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, many=False,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def follow_action(request):
    username = request.data.get('username')
    profile = request.user
    if not profile:
        return Response({'error': 'Annonymous User'}, status=status.HTTP_400_BAD_REQUEST)
    f_user = User.objects.get(username=username)

    if f_user in profile.following.all():
        profile.following.remove(f_user)
        return Response({'follow':False, "followers": f_user.followed.count()})
    else: 
        profile.following.add(f_user)
        Notification.objects.get_or_create(notification_type="F",  to_user=f_user, from_user=profile)
        return Response({'follow':True, "followers":f_user.followed.count()})

class EditUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  
        return Response("Value error", status=status.HTTP_406_NOT_ACCEPTABLE)

class DeleteUserView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
   
    def patch(self,request):
        user = request.user
        #try:
        user.delete()
        return Response("Account Deleted!", status=status.HTTP_200_OK)
        #except:
        #   return Response("Value error", status=status.HTTP_406_NOT_ACCEPTABLE)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User 
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user 
        return obj 

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print(serializer.data.get("old_password"))
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response("Old password is wrong!",  status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Password changed succesfully!", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)