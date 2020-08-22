from django import forms
from .models import InvoiceMaster, InvoiceItemsMaster

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = InvoiceMaster
        fields = ('inv_invoice_num','inv_vendor_name','inv_invoice_date','inv_invoice_file', 'inv_user')

    def __init__(self, *args, **kwargs):
        super(InvoiceForm,self).__init__(*args, **kwargs)

class InvoiceItemsListForm(forms.ModelForm):
    class Meta:
        model = InvoiceItemsMaster
        fields = ('itx_item_desc','itx_item_quantity', 'itx_item_rate','itx_inv_num')

    def __init__(self, *args, **kwargs):
        super(InvoiceItemsListForm,self).__init__(*args, **kwargs)
