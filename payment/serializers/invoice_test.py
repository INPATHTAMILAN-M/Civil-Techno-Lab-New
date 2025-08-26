from rest_framework import serializers
from payment.models import Invoice_Test, Invoice
from general.models import Test
from account.models import Employee

from rest_framework import serializers
from bs4 import BeautifulSoup
import re
from django.conf import settings

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class InvoiceTestListSerializer(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    material_name = serializers.SerializerMethodField()
    qty = serializers.SerializerMethodField()

    class Meta:
        model = Invoice_Test
        fields = ['id','invoice','invoice_no','material_name','test','test_name','qty','price_per_sample','total','invoice_image','customer','created_date','completed']   

    def get_test_name(self,obj):
        return str(obj.test)
    
    def get_material_name(self,obj):
        return str(obj.test.material_name)
    
    def get_qty(self,obj):
        return str(int(obj.quantity))
    


class InvoiceTestDetailSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    invoice = InvoiceSerializer()
    primary_signature = SignatureSerializer()
    secondary_signature = SignatureSerializer()
    final_html = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    without_signature = serializers.SerializerMethodField()
    without_header_footer = serializers.SerializerMethodField()
    is_old_invoice_format = serializers.SerializerMethodField()

    class Meta:
        model = Invoice_Test
        fields = '__all__'

    def get_count(self, obj):
        return str(obj.count)

    def get_is_old_invoice_format(self, obj):
        return obj.invoice.is_old_invoice_format

    def remove_headers(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        header_sources = getattr(settings, 'INVOICE_HEADER_SOURCES', [
            f'{settings.BACKEND_DOMAIN}/static/header-hammer.png',
            f'{settings.BACKEND_DOMAIN}/static/header.gif'
        ])

        for src in header_sources:
            img = soup.find('img', {'src': src})
            if img:
                parent_tr = img.find_parent('tr')
                if parent_tr:
                    parent_tr.decompose()
                else:
                    img.decompose()
        return soup

    def add_page_breaks_and_update_numbers(self, soup, signature_block):
        first_table_html = str(soup.select_one("table:nth-of-type(1)"))
        count = 1
        for p_tag in soup.find_all('p', text=re.compile(r'Page Break', re.IGNORECASE)):
            count += 1
            updated = first_table_html.replace('Page No: 1', f'Page No: {count}')
            updated = updated.replace('<table', '<table style="margin-bottom:10px !important" class="pagebreak"')
            new_content = BeautifulSoup(updated, 'html.parser')
            trs = new_content.find_all('tr')
            if len(trs) >= 3:
                trs[2].decompose()
            p_tag.replace_with(new_content)

        soup.append(BeautifulSoup(signature_block, 'html.parser'))
        return str(soup)

    def get_signature_html(self, obj, signature, hidden=False, label="Covai Civil Lab Private Limited"):
        
        if obj.id == 33:
            return f"""
                <p id=\"dynamic-signature\">/p>
                <p style=\"font-size:12px\">/p>
                <p style=\"font-size:12px\"></p>
            """
        else:
            if not signature:
                return "<p></p>"
            if hidden:
                img_tag = '<img style="visibility: hidden;" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" height="38px" width="38px">'
            else:
                img_tag = f'<img src="{settings.BACKEND_DOMAIN}/media/{signature.signature}" height="150px" width="150px">'
            return f"""
                <p id=\"dynamic-signature\">{img_tag}</p>
                <p style=\"font-size:12px\"><strong>{signature}<br>{signature.role}</strong></p>
                <p style=\"font-size:12px\"><strong>{label}</strong></p>
            """

    def get_authorised_block(self):
        return """
            <p id=\"dynamic-signature\"></p>
            <p style=\"font-size:12px\"><strong><br><br>Authorised Signatory</strong></p>
            <p style=\"font-size:12px\"><strong>Covai Civil Lab Private Limited</strong></p>
        """

    def get_signature_block(self, obj, hidden=False, footer=True):
        if obj.primary_signature:
            if obj.without_primary_signature:
                left_block = self.get_signature_html(obj,obj.primary_signature, hidden=True)
            else:
                left_block = self.get_signature_html(obj,obj.primary_signature)
        elif obj.primary_authorised_signature:
            left_block = self.get_authorised_block()
        else:
            left_block = "<p></p>"

        if obj.secondary_signature:
            if obj.without_secondary_signature:
                right_block = self.get_signature_html(obj,obj.secondary_signature, hidden=True)
            else:
                right_block = self.get_signature_html(obj,obj.secondary_signature)
        elif obj.secondary_authorised_signature:
            right_block = self.get_authorised_block()
        else:
            right_block = "<p></p>"

        qr_image_src = obj.invoice_image.url if hasattr(obj.invoice_image, 'url') else f"{settings.BACKEND_DOMAIN}/{obj.invoice_image}"
        footer_img = f'<p><img alt="Logo" src="{settings.BACKEND_DOMAIN}/static/test-footer.png" style="width:100%" /></p>' if footer else ''

        return f"""
        <figure class=\"table\">
            <table cellpadding=\"0\" cellspacing=\"1\" border=\"0\" style=\"border:none !important; border-spacing:0.6pt; width:100%\">
                <tr>
                    <td width=\"40%\" style=\"border:0 !important;\">{left_block}</td>
                    <td width=\"40%\" style=\"border:0 !important;\">{right_block}</td>
                    <td width=\"20%\" style=\"border:0 !important;\" class=\"qr-code\">
                        <img src=\"{qr_image_src}\">
                    </td>
                </tr>
                <tr><td colspan=\"3\"><hr style=\"color: #000;\"></td></tr>
                <tr><td colspan=\"3\" style=\"border-style:inset; border-width:0.75pt;\">{footer_img}</td></tr>
            </table>
        </figure>
        """

    def get_final_html(self, obj):
        if not (obj.primary_signature or obj.secondary_signature or obj.primary_authorised_signature or obj.secondary_authorised_signature):
            return obj.report_template

        html = obj.report_template.replace('Page Break', '<div class="pagebreak"> </div>')
        block = self.get_signature_block(obj, hidden=False)
        return html + block

    def get_without_signature(self, obj):
        if not (obj.primary_signature or obj.secondary_signature or obj.primary_authorised_signature or obj.secondary_authorised_signature):
            return None
        soup = self.remove_headers(obj.report_template)
        block = self.get_signature_block(obj, footer=False)
        return self.add_page_breaks_and_update_numbers(soup, block)

    def get_without_header_footer(self, obj):
        if not (obj.primary_signature or obj.secondary_signature or obj.primary_authorised_signature or obj.secondary_authorised_signature):
            return None
        soup = self.remove_headers(obj.report_template)
        block = self.get_signature_block(obj, hidden=False, footer=False)
        return self.add_page_breaks_and_update_numbers(soup, block)

class InvoiceTestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_Test
        fields = ['quantity', 'total', 'price_per_sample', 'invoice', 'test']

class InvoiceTestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_Test
        fields = '__all__'
        read_only_fields = ['created_by', 'invoice_image', 'report_template']

    def update(self, instance, validated_data):
        # Perform default update first
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Only modify report_template if signature exists and report_template is present
        if instance.primary_signature and instance.report_template:
            soup = BeautifulSoup(instance.report_template, 'html.parser')
            div_to_modify = soup.find('p', class_='dynamic-signature')

            if div_to_modify:
                img_element = soup.new_tag(
                    'img',
                    src=f'{settings.BACKEND_DOMAIN}/media/{instance.signature.signature}'
                )
                div_to_modify.replace_with(img_element)
                instance.report_template = soup.prettify()
                instance.save()

        return instance
