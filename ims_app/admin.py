from django.contrib import admin
from .models import InvoiceMaster, InvoiceItemsMaster

admin.site.register(InvoiceMaster)
admin.site.register(InvoiceItemsMaster)