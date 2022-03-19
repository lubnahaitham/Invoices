from decimal import Decimal
from itertools import product
import json
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .decorators import unauthenticated_user
from .forms import InvoiceForm, SettingForm, ProductForm, CreateUserForm
from .models import Setting, Invoice, Product
from django.db.models import Q
from django.utils import timezone

from . import models
import base64
import pyqrcode
import png
from pyqrcode import QRCode

# Create your views here.

def home(request):
    return render(request, 'homepage.html')


@unauthenticated_user
# @admin_only
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('/login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/login')


def setting_create(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = SettingForm()
        else:
            setting = get_object_or_404(Setting, pk=id)
            form = SettingForm(instance=setting)
        return render(request, "setting/setting_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = SettingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/invoice/list')


# Product
def product_list(request):
    context = {'product_list': Product.objects.all()}
    return render(request, "product/product_list.html", context)


def product_view(request, id):
    context = {'product_view': Product.objects.get(pk=id)}
    return render(request, "product/product_view.html", context)


def product_create(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ProductForm()
        else:
            product = get_object_or_404(Product, pk=id)
            form = ProductForm(instance=product)
        return render(request, "product/product_create.html", {'form': form})
    else:
        if request.method == "POST":
            if id == 0:
                form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/product/list')


def product_update(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/product/list')

    context = {'form': form}
    return render(request, 'product/product_update.html', context)


def product_delete(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect('/product/list')


# Pos
def invoice_pos_list(request):
    invoice_list = Invoice.objects.all()
    # attribute_values = zip(invoice_list)
    context = {'invoice_list': invoice_list}
    return render(request, "pos/pos_list.html", context)


def invoice_view(request, id):
    setting_data_view=Setting.objects.get(id=1)
    product_data = Product.objects.get(pk=id)
    invoice_data = Invoice.objects.get(pk=id)
    qrt="f"
    comp=get_tl_vfor_value(1,str(setting_data_view.organization_name))#get_tl_vfor_value(1,"Bobs Records")
    vat_num = get_tl_vfor_value(2,str(setting_data_view.vat_number))#get_tl_vfor_value(2,"310122393500003")
    order_date = get_tl_vfor_value(3,str(invoice_data.invoice_issue_date))#get_tl_vfor_value(3,"2022-04-25T15:30:00Z")
    tot_amount = get_tl_vfor_value(4,str(invoice_data.total_amount_due))#get_tl_vfor_value(4,"1000.00")
    vat_amount = get_tl_vfor_value(5, str(invoice_data.total_vat))#get_tl_vfor_value(5, "150.00")
    tagsbuff = comp+vat_num+order_date+tot_amount+vat_amount
    print(tagsbuff)
    conv_bytes = bytes.fromhex(tagsbuff.hex())
    qrt1 = base64.b64encode(conv_bytes)
    qrt=str(qrt1.decode())
    print(qrt)
    url = pyqrcode.create(qrt)
    png = url.png('static/images/encoded_img2.png', scale = 4)
    
    context = {'setting_data_view': setting_data_view,
               'invoice_data': invoice_data, 'product_data': product_data, 'png':png}
    return render(request, "pos/pos_view.html", context)



def get_tl_vfor_value(tagnum, tagvalue):
    tagBuf = int(tagnum).to_bytes(1,byteorder="big")
    tagValueLenBuf= int(len(str(tagvalue))).to_bytes(1,byteorder="big")
    tagValueBuf = bytes(str(tagvalue),'utf-8')
    bufarr = tagBuf+tagValueLenBuf+tagValueBuf
    return bufarr

# def invoice_create(request):
#     setting_data = Setting.objects.get(id=1)
#     invoice_form = InvoiceForm(request.POST or None)
#     products = list(Product.objects.all())

#     context = {
#         "invoice_form": invoice_form,
#         "setting_data": setting_data,
#         "products": products,

#     }


#     if all([invoice_form.is_valid()]):
#         parent = invoice_form.save(commit=False)
#         parent.save()


#         return redirect('/invoice/list')
#     return render(request, "pos/pos_create.html", context)

# polldict={}

def invoice_create(request):
    setting_data = Setting.objects.get(id=1)
    products = list(Product.objects.all())
    invoice_form = InvoiceForm(request.POST or None)
    date_of_supply = request.POST.get('date_of_supply')
    branch = request.POST.get('branch')
    salesman_name = request.POST.get('salesman_name')
    page_number = request.POST.get('page_number')

    # buyer data
    buyer_organization_name = request.POST.get('buyer_organization_name')
    building_number = request.POST.get('building_number')
    street_name = request.POST.get('street_name')
    district = request.POST.get('district')
    city = request.POST.get('city')
    country = request.POST.get('country')
    postal_code = request.POST.get('postal_code')
    additional_number = request.POST.get('additional_number')
    vat_number = request.POST.get('vat_number')
    other_buyer_id = request.POST.get('other_buyer_id')


    discount = request.POST.get('discount')
    total_vat = request.POST.get('total_vat')
    total_taxable_amount_exclude_vat = request.POST.get('total_taxable_amount_exclude_vat')
    total_amount_due = request.POST.get('total_amount_due')
    total = request.POST.get('total')

    
    # total_exclude_vat = request.POST.get('total_exclude_vat')

    quantity= request.POST.get('quant')

    # price = request.POST.get('price')
    
   
    taxable_amount = request.POST.get('taxable_amount')

    tax_amount = request.POST.get('tax_amount')

    tax_rate = request.POST.get('tax')

    sub_total = request.POST.get('sub_total')



    new_invoice = models.Invoice(date_of_supply=date_of_supply, branch=branch, salesman_name=salesman_name,
                                 page_number=page_number, buyer_organization_name=buyer_organization_name, 
                                 building_number=building_number, street_name=street_name, district=district, city=city, country=country,
                                 postal_code=postal_code, additional_number=additional_number, vat_number=vat_number, 
                                 other_buyer_id=other_buyer_id, discount=discount,
                                 total_taxable_amount_exclude_vat=total_taxable_amount_exclude_vat, total_vat=total_vat,  
                                 total_amount_due=total_amount_due, total=total, quantity=quantity,
                                 tax_amount=tax_amount, tax_rate=tax_rate, 
                                 sub_total=sub_total, taxable_amount=taxable_amount)
    new_invoice.save()

  
    context = {
        "setting_data": setting_data,
        "products": products,
        "invoice_form": invoice_form,

    }

    if all([invoice_form.is_valid()]):
        parent = invoice_form.save(commit=False)
        parent.save()


        return redirect('/invoice/list')
    return render(request, "pos/pos_create.html", context)


    

  



def invoice_delete(request, id):
    invoice = get_object_or_404(Invoice, pk=id)
    invoice.delete()
    return redirect('/invoice/list')

