from django.db import models

class InvoiceMaster(models.Model):
    inv_invoice_num = models.CharField(max_length=10, primary_key=True)
    inv_vendor_name = models.CharField(max_length=145, null=True)
    inv_invoice_date = models.DateField()
    inv_invoice_file = models.FileField(upload_to='media/')
    inv_user = models.CharField(max_length=35)

class InvoiceItemsMaster(models.Model):
    itx_item_desc = models.CharField(max_length=150)
    itx_item_quantity = models.IntegerField()
    itx_item_rate = models.FloatField()
    itx_inv_num = models.ForeignKey(InvoiceMaster,on_delete=models.CASCADE)
