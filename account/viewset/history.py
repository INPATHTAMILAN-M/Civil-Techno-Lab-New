from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from account.serializers import HistorySerializer
from payment.pagination import CustomPagination

class GenericHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorySerializer
    pagination_class = CustomPagination  

    def get_queryset(self):
        # The model class will be passed in via the `as_viewset()` method below
        return self.model.history.all()

    @classmethod
    def as_viewset(cls, model):
        class ConcreteHistoryViewSet(cls):
            pass
        ConcreteHistoryViewSet.model = model
        return ConcreteHistoryViewSet
