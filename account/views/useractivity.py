from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import  UserActivity
from account.serializers import UserLogGetSerializer


class Userlogs(APIView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        user_logs = UserActivity.objects.all()
        serializer = UserLogGetSerializer(user_logs, many=True)
        return Response(serializer.data)