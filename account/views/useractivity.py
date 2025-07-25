from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import  UserActivity
from account.serializers import UserLogGetSerializer
from payment.pagination import CustomPagination


class Userlogs(APIView):
    http_method_names = ['get', 'post']
    
    def get(self, request, *args, **kwargs):
        user_logs = UserActivity.objects.all().order_by('-id')  # or any relevant field
        paginator = CustomPagination()
        paginated_logs = paginator.paginate_queryset(user_logs, request)
        serializer = UserLogGetSerializer(paginated_logs, many=True)
        return paginator.get_paginated_response(serializer.data)
