from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.log_user_action import log_user_activity

from account.serializers import (
                ChangePasswordSerializer,
                LoginSerializer
                )

class ChangePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_new_password = serializer.validated_data.get('confirm_new_password')

            # Check if the old password is correct
            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the new passwords match
            if new_password != confirm_new_password:
                return Response({'detail': 'New passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Update the session to prevent logout
            update_session_auth_hash(request, user)

            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class Login_View(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                log_user_activity(user=user, action="LOGIN",
                                  ip=request.META.get('HTTP_X_FORWARDED_FOR'),details=request.META)
                if User.objects.filter(groups__name="Admin",id=user.id):
                    is_admin = True                    
                else:
                    is_admin = False

                return Response({'token': token.key,'name':str(user),'is_admin':is_admin}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)