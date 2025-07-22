from rest_framework import serializers
from payment.models import Invoice_Test
from general.models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
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

    class Meta:
        model = Invoice_Test
        fields = '__all__'

class InvoiceTestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_Test
        fields = ['quantity', 'total', 'price_per_sample', 'invoice', 'test']

class InvoiceTestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_Test
        fields = '__all__'
        read_only_fields = ['created_by', 'invoice_image', 'report_template']
