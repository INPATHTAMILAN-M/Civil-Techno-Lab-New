from payment.serializers.quatation_item import (
    QuotationItemGetSerializer,
    QuotationItemUpdateSerializer,
    QuotationItemListSerializer,
    QuotationItemDeleteSerializer,
    QuotationItemBulkCreateSerializer,
)
from payment.serializers.quotation import (
    QuotationCreateSerializer,
    QuotationRetrieveSerializer,
    QuotationListSerializer,
    QuotationUpdateSerializer,
)
from payment.serializers.invoice_old import *
from payment.serializers.invoice_report import (
    InvoiceReportCreateSerializer,
    InvoiceReportDetailSerializer,
    InvoiceReportListSerializer,
    InvoiceReportUpdateSerializer,
)
from payment.serializers.receipt import (
    ReceiptListSerializer,
    ReceiptCreateSerializer,
    ReceiptDetailSerializer,
    ReceiptUpdateSerializer,
)
from payment.serializers.customer_discount import (
    CustomerDiscountListSerializer,
    CustomerDiscountCreateSerializer,
    CustomerDiscountUpdateSerializer,
    CustomerDiscountRetrieveSerializer
)
from payment.serializers.invoice_test import (
    InvoiceTestListSerializer,
    InvoiceTestDetailSerializer,
    InvoiceTestCreateSerializer,
    InvoiceTestUpdateSerializer,
)
from payment.serializers.quotation_report import (
    QuotationReportCreateSerializer,
    QuotationReportDetailSerializer,
    QuotationReportListSerializer,
    QuotationReportUpdateSerializer,
)
from payment.serializers.quotation import QuotationSerializer
from payment.serializers.test import (
    TestCreateSerializer,
    TestUpdateSerializer,
    TestListSerializer,
    TestDetailSerializer,
)
from payment.serializers.invoice import (
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    InvoiceListSerializer,
    InvoiceRetrieveSerializer,
    
)
from payment.serializers.material import (
    MaterialListSerializer,
    MaterialCreateSerializer,
    MaterialUpdateSerializer,
    MaterialDetailSerializer,
)

from payment.serializers.invoice_discount import (
    InvoiceDiscountCreateSerializer,
    InvoiceDiscountUpdateSerializer,
    InvoiceDiscountDetailSerializer,
    InvoiceDiscountListSerializer,
)
from payment.serializers.invoice_file import (
    InvoiceFileCreateSerializer,
    InvoiceFileUpdateSerializer,
    InvoiceFileRetrieveSerializer,
    InvoiceFileListSerializer
)

