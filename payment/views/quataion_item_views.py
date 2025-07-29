from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, 
    UpdateAPIView, ListAPIView, DestroyAPIView
)
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from payment.models import QuotationItem
from payment.filters.quotation_item import QuotationItemFilter
from payment.serializers.quatation_item import (
    QuotationItemBulkCreateSerializer, 
    QuotationItemUnifiedSerializer,
    QuotationItemDeleteSerializer
)
from ..serializers import (
    QuotationItemListSerializer,
    QuotationItemGetSerializer,
    QuotationItemUpdateSerializer,
)
from rest_framework.response import Response
from rest_framework import serializers, status

# Create API View for Creating Quotation Items
class QuotationItemCreateView(CreateAPIView):
    queryset = QuotationItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # Return the appropriate serializer based on input type
        if isinstance(self.request.data, dict):
            return QuotationItemUnifiedSerializer
        elif isinstance(self.request.data, list):
            return QuotationItemBulkCreateSerializer
        raise serializers.ValidationError("Invalid input type. Expected a dictionary or list.")

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, dict):  # Single object
            serializer = QuotationItemUnifiedSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif isinstance(request.data, list):  # Bulk objects
            serializer = QuotationItemBulkCreateSerializer(
                data={"items": request.data}, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Quotation items created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Invalid input type. Expected single or bulk JSON data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

# List API View for Listing All Quotation Items
class QuotationItemListView(ListAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuotationItemFilter


# Retrieve API View for Getting a Single Quotation Item
class QuotationItemRetrieveView(RetrieveAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemGetSerializer
    permission_classes = [permissions.IsAuthenticated]


# Update API View for Updating a Quotation Item
class QuotationItemUpdateView(UpdateAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Quotation Item  updated successfully"}, status=status.HTTP_200_OK)


# Delete API View for Deleting a Quotation Item
class QuotationItemDeleteView(DestroyAPIView):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Quotation item deleted successfully"},
            status=status.HTTP_200_OK
        )

