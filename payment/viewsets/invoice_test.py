import os
from django.conf import settings
import qrcode
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from payment.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from payment.models import Invoice_Test
from payment.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from payment.filters import InvoiceTestFilter


class InvoiceTestViewSet(viewsets.ModelViewSet):
    queryset = Invoice_Test.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = InvoiceTestFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceTestCreateSerializer
        if self.action == 'list':
            return InvoiceTestListSerializer
        if self.action in ['update', 'partial_update']:
            return InvoiceTestUpdateSerializer
        return InvoiceTestDetailSerializer  
    
    def get_permissions(self):
        if self.action in ['retrieve','list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        pagination_param = request.query_params.get('pagination', 'true').lower()

        queryset = self.filter_queryset(self.get_queryset())

        if pagination_param == 'false':
            MAX_RESULTS = 300
            queryset = queryset[:MAX_RESULTS]
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)

        instances = serializer.save(created_by=request.user, modified_by=request.user)

        # If only one object is created, wrap it in a list for consistency
        if not isinstance(instances, list):
            instances = [instances]

        for i_test in instances:
            template = i_test.test.material_name.template or ''
            invoice = i_test.invoice
            customer = invoice.customer

            # Replace placeholders
            template = template.replace('Test Order', f'Test Order: {invoice.invoice_no}')
            template = template.replace('CUSTOMERDETAILS', f'<p>{customer.customer_name}</p><p>{customer.address1}</p>')
            template = template.replace('Date :', f'Date : {i_test.created_date.strftime("%d/%m/%Y")}')
            template = template.replace('Place of Testing Name', str(invoice.place_of_testing))
            template = template.replace('Project Name', str(invoice.project_name))

            # Header image and ULR logic
            if i_test.test.material_name.material_name == 'Rebound Hammer':
                template = template.replace(
                    '<td colspan="2">&nbsp;</td>',
                    f'<td colspan="2"><img alt="Logo" src="{settings.BACKEND_DOMAIN}/static/header-hammer.png" style="width:100%" /></td>',
                    1
                )
                template = template.replace('ULR:', f'ULR: {i_test.ulr}')
            else:
                template = template.replace(
                    '<td colspan="2">&nbsp;</td>',
                    f'<td colspan="2"><img alt="Logo" src="{settings.BACKEND_DOMAIN}/static/header.gif" style="width:100%" /></td>',
                    1
                )

            # QR code generation
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr_url = f"{settings.QR_DOMAIN}/invoice/viewtestreport?id={i_test.id}"
            qr.add_data(qr_url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            qr_dir = os.path.join(settings.MEDIA_ROOT, "invoice_test")
            os.makedirs(qr_dir, exist_ok=True)
            qr_filename = f"invoice_{i_test.id}.png"
            qr_path = os.path.join(qr_dir, qr_filename)
            qr_img.save(qr_path)

            qr_relative = f"media/invoice_test/{qr_filename}"
            i_test.invoice_image = qr_relative

            # Embed QR image in HTML
            qr_img_tag = f'<img height="120" width="120" src="{settings.BACKEND_DOMAIN}/{qr_relative}">'
            template = template.replace('qr code', qr_img_tag)

            # Final save
            i_test.report_template = template
            i_test.save()

        output_serializer = InvoiceTestDetailSerializer(instances, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
