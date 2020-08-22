from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from .forms import InvoiceForm, InvoiceItemsListForm

from django.contrib.auth.models import User
from .models import InvoiceMaster, InvoiceItemsMaster

from datetime import datetime, date
from django.core.mail import send_mail

import random
import string

inv_dt = date.today().isoformat()
mail_sub = 'New Invoice Generated'

@unauthenticated_user
def loginPage(request):
    template = 'ims_app/login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['name'] = username

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            if user.groups.filter(name='agent').exists():
                return redirect(reverse(index))
            elif user.groups.filter(name='manager').exists():
                return redirect(reverse(viewallinvoices))

        else:
            messages.warning(request, "Invalid Credentials")
            return redirect('login')
    return render(request, template)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles='agent')
def index(request):
    return redirect('viewagentinvoice')


@login_required(login_url='login')
@allowed_users(allowed_roles='agent')
def newinvoice(request):
    uname = request.session.get('name')
    return render(request, 'ims_app/newinvoice.html', {'inv_invoice_date': inv_dt, 'uname': uname})


@login_required(login_url='login')
@allowed_users(allowed_roles='agent')
def loadinvoice(request):
    inv_dt = date.today().isoformat()
    if request.method == 'POST':
        inv_invoice_num = request.POST.get('inv_invoice_num')
        inv_vendor_name = request.POST.get('inv_vendor_name')
        inv_invoice_file = request.FILES['inv_invoice_file']
        inv_user = request.session.get('name')
        agent_name = request.user.get_full_name()
        invoiceObj = InvoiceMaster(inv_invoice_num=inv_invoice_num, inv_vendor_name=inv_vendor_name, inv_invoice_date=inv_dt,
                                   inv_invoice_file=inv_invoice_file, inv_user=inv_user)
        invoiceObj.save()

        mail_body = {"Invoice Number": inv_invoice_num, "Invoice Date": inv_dt,
                     "Agent Name": agent_name, "Invoice File": inv_invoice_file}
        body_str = str(mail_body)

        send_mail(
            mail_sub,
            body_str,
            'imsadm21@gmail.com',
            ['makwana7a@gmail.com'],
            fail_silently=False)
        return redirect('newinvoice')


@login_required(login_url='login')
@allowed_users(allowed_roles='agent')
def fillinvoice(request):
    uname = request.session.get('name')
    return render(request, 'ims_app/fillinvoice.html', {'uname': uname})


@login_required(login_url='login')
@allowed_users(allowed_roles='agent')
def fillindetails(request):
    if request.method == 'GET':
        inv_invoice_num = request.GET.get('inv_invoice_num')
        inv_details = InvoiceMaster.objects.get(inv_invoice_num=inv_invoice_num)
    return render(request, 'ims_app/fillindetails.html', {'inv_details': inv_details})


@login_required(login_url='login')
@allowed_users(allowed_roles='agent')
def saveindetails(request):
    if request.method == 'POST':
        itx_inv_num = request.POST.get('itx_inv_num')
        inv_details = InvoiceMaster.objects.get(inv_invoice_num=itx_inv_num)

        itx_item_desc = request.POST.getlist('itx_item_desc')
        itx_item_quantity = request.POST.getlist('itx_item_quantity')
        itx_item_rate = request.POST.getlist('itx_item_rate')

        x = min([len(itx_item_desc), len(itx_item_quantity), len(itx_item_rate)])
        for i in range(0,x):
            itemsObj = InvoiceItemsMaster(itx_inv_num=inv_details, itx_item_desc=itx_item_desc[i],
                                      itx_item_quantity=itx_item_quantity[i], itx_item_rate=itx_item_rate[i])
            itemsObj.save()
    return redirect('newinvoice')

@login_required(login_url='login')
@allowed_users(allowed_roles='agent')
def viewagentinvoice(request, id=0):
    uname = request.session.get('name')
    data = InvoiceMaster.objects.filter(inv_user=uname)
    return render(request, 'ims_app/viewaginvoices.html', {'data': data, 'uname': uname})


@login_required(login_url='login')
@allowed_users(allowed_roles='manager')
def viewallinvoices(request):
    uname = request.session.get('name')
    data = InvoiceMaster.objects.all()
    return render(request, 'ims_app/viewallinvoices.html', {'data': data, 'uname': uname})
