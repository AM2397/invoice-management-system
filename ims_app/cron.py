import os
from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail

from .models import InvoiceMaster, InvoiceItemsMaster
from django.contrib.auth.models import User

from datetime import datetime, date, timedelta
import string

pre_dt = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

class AutoEmail(CronJobBase):

    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ims_app.auto_email'

    def do(self):
        data = InvoiceMaster.objects.filter(inv_invoice_date=pre_dt).count()
        usrObj = User.objects.get(username='acme_ims')
        mgr_nm = usrObj.get_full_name()

        mail_sub = {'Invoice Summary' : pre_dt}
        sub_str = str(mail_sub)
        mail_subject = str(sub_str).replace("{","").replace("}", "").replace("'","")

        salutation = {'Dear ': mgr_nm}
        slt_str = str(salutation).replace("{","").replace("}", "").replace("'","").replace(":", "")
        slt_str = slt_str + ','

        body = {'Here is a summary for': pre_dt, 'No. of invoices': data, 'Total amount': 10000}
        body_str = str(body).replace("{","").replace("}", "").replace("'","").replace(",","\n")
        mail_body = slt_str + '\n' + body_str
        
        send_mail(
            mail_subject,
            mail_body,
            os.environ.get('EMAIL_HOST_USER'),
            ['makwana7a@gmail.com'],
            fail_silently=False)