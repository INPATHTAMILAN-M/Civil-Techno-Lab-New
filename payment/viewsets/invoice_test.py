import os
from django.conf import settings
import qrcode
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        validated_data['created_by'] = request.user
        validated_data['modified_by'] = request.user

        # Manually build the instance (without saving yet)
        instance = Invoice_Test(**validated_data)

        # Generate report template and QR image path
        report_template, invoice_img_path = self._build_invoice_template(instance)
        instance.report_template = report_template
        instance.invoice_image = invoice_img_path

        # Save only once
        instance.save()

        # Return response
        output_serializer = InvoiceTestDetailSerializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def _build_invoice_template(self, instance):
        """Builds the updated HTML template and returns image path."""
        template = instance.test.material_name.template or ""
        template = self._replace_basic_fields(template, instance)
        template = self._add_header_image(template, instance)
        template, qr_path = self._add_qr_code(template, instance)
        return template, qr_path

    def _replace_basic_fields(self, template, instance):
        invoice = instance.invoice
        customer = invoice.customer

        replacements = {
            'Test Order': f'Test Order: {invoice.invoice_no}',
            'CUSTOMERDETAILS': f'<p>{customer.customer_name}</p><p>{customer.address1}</p>',
            'Date :': f'Date : {invoice.date.strftime("%d-%m-%Y")}',
            'Place of Testing Name': str(invoice.place_of_testing),
            'Project Name': str(invoice.project_name),
        }

        for key, value in replacements.items():
            template = template.replace(key, value)

        return template

    def _add_header_image(self, template, instance):
        material = instance.test.material_name.material_name
        if material == 'Rebound Hammer':
            header_img = f'<td colspan="2"><img alt="Logo" src="{settings.BACKEND_DOMAIN}/static/header-hammer.png" style="width:100%" /></td>'
            template = template.replace('ULR:', f'ULR: {instance.ulr}')
        else:
            header_img = f'<td colspan="2"><img alt="Logo" src="{settings.BACKEND_DOMAIN}/static/header.gif" style="width:100%" /></td>'

        return template.replace('<td colspan="2">&nbsp;</td>', header_img, 1)

    def _add_qr_code(self, template, instance):
        qr_url = f"{settings.QR_DOMAIN}/invoice/viewtestreport?id={instance.id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        qr_dir = os.path.join(settings.MEDIA_ROOT, "invoice_test")
        os.makedirs(qr_dir, exist_ok=True)
        qr_filename = f"invoice_{instance.id}.png"
        qr_path = os.path.join(qr_dir, qr_filename)
        qr_image.save(qr_path)

        # Replace "qr code" placeholder in the HTML
        qr_html = f'<img height="120" width="120" src="{settings.BACKEND_DOMAIN}/invoice_test/{qr_filename}">'
        template = template.replace('qr code', qr_html)

        return template, f"invoice_test/{qr_filename}"