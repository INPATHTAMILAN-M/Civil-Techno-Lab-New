from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from payment.pagination import CustomPagination
from account.serializers import HistorySerializer

class GenericHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        if not hasattr(self, 'model') or self.model is None:
            raise ValueError("Model not specified for history viewset")
        
        queryset = self.model.history.all()

        params = self.request.query_params

        # Date range filtering
        if all(k in params for k in ['from_date', 'to_date']):

            try:
                from_date = datetime.strptime(params['from_date'], '%Y-%m-%d').date()
                to_date = datetime.strptime(params['to_date'], '%Y-%m-%d').date()
                queryset = queryset.filter(
                    history_date__gte=from_date,
                    history_date__lte=to_date
                )
            except ValueError:
                pass

        # Individual date filters (fallback)
        elif 'from_date' in params:
            try:
                from_date = datetime.strptime(params['from_date'], '%Y-%m-%d').date()

                queryset = queryset.filter(history_date__gte=from_date)
            except ValueError:
                pass
                
        elif 'to_date' in params:
            try:
                to_date = datetime.strptime(params['to_date'], '%Y-%m-%d').date()
                queryset = queryset.filter(history_date__lte=to_date)
            except ValueError:
                pass

        # History type filtering
        if 'history_type' in params:
            queryset = queryset.filter(history_type=params['history_type'])

        return queryset

    @classmethod
    def as_viewset(cls, model):
        class ConcreteHistoryViewSet(cls):
            pass
        ConcreteHistoryViewSet.model = model
        return ConcreteHistoryViewSet
    