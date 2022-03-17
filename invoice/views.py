from decimal import Decimal
from itertools import product
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.forms import inlineformset_factory
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

    quantity= request.POST.get('quant')

    price = request.POST.get('price')
    
    discount = request.POST.get('discount')

    total_vat = request.POST.get('total_vat')

    taxable_amount = request.POST.get('taxable_amount')

    tax_amount = request.POST.get('tax_amount')

    tax_rate = request.POST.get('tax')

    total_taxable_amount_exclude_vat = request.POST.get('total_taxable_amount_exclude_vat')

    total_exclude_vat = request.POST.get('total_exclude_vat')

    total_amount_due = request.POST.get('total_amount_due')

    sub_total = request.POST.get('sub_total')

    total = request.POST.get('total')

    new_invoice = models.Invoice(date_of_supply=date_of_supply, branch=branch, salesman_name=salesman_name,
                                 page_number=page_number, buyer_organization_name=buyer_organization_name, 
                                 building_number=building_number, street_name=street_name, district=district, city=city, country=country,
                                 postal_code=postal_code, additional_number=additional_number, vat_number=vat_number, 
                                 other_buyer_id=other_buyer_id, quantity=quantity, price=price, discount=discount,
                                 total_taxable_amount_exclude_vat=total_taxable_amount_exclude_vat, total_vat=total_vat,
                                 taxable_amount=taxable_amount, tax_amount=tax_amount, tax_rate=tax_rate,
                                 total_exclude_vat=total_exclude_vat, total_amount_due=total_amount_due, sub_total=sub_total, total=total)
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


# def pos(request):

#     # # get all Categories
#     parent_cate_id = request.GET.get('parent_cate_id')
#     parent_categories = Categories.objects.filter(pos= True, digital_menu =True, is_parent =True).all()

#     try:
#         current_parent_cate=Categories.objects.get(id=parent_cate_id)
#         child_categories = Categories.objects.filter(pos= True, digital_menu =True, is_parent =False, parent=current_parent_cate.name).all()
#         products = Product.objects.filter(Q(Category_id__parent=current_parent_cate.name) | Q(Category_id=current_parent_cate) , pos=True).all()
#     except:
#         current_parent_cate=''
#         child_categories=''
#         products=""


#     #child_categories = Categories.objects.filter(pos= True, digital_menu =True, is_parent =False, parent=).all()


#     # get product object by id
#     cate_id = request.GET.get('cate_id')
#     if cate_id:
#         products = Products.objects.filter(Category_id=cate_id, digital_menu =True).all()

#     pid = request.GET.get('productId')
#     action = request.GET.get('action')
#     order_id = request.GET.get('orderId')
#     order2 = Orders.objects.filter(created_by=request.user.username, status='Prepared')
#     qrt="f"


#     product = None
#     total= 0
#     tax =0
#     sub_total =0
#     items = None
#     discount =0
#     net_price=0
#     branch= None
#     total_price=0


#     try:
#             orderId = request.GET.get('orderId')
#             order = Orders.objects.get(id=orderId)
#             items = OrderItems.objects.filter(order=order)

#     except:
#         order, created = Orders.objects.get_or_create(status = 'Started', created_by=request.user.username)
#     #qrt= "https://demo.kuppitek.com/pos/qrcode/"+str(order.id)
#    # conv_bytes = bytes("qrt", 'utf-8')
#     order1 = order
#     amount_without_vat=0
#     # order_total_amount=float(order1.total_amount)
#     # order_tax=float(order1.tax)
#     # comp=get_tl_vfor_value(1,str(company.coffee_name))#get_tl_vfor_value(1,"Bobs Records")
#     # vat_num = get_tl_vfor_value(2,str(company.vat_num))#get_tl_vfor_value(2,"310122393500003")
#     # order_date = get_tl_vfor_value(3,str(order1.created_date))#get_tl_vfor_value(3,"2022-04-25T15:30:00Z")
#     # tot_amount = get_tl_vfor_value(4,str(order_total_amount))#get_tl_vfor_value(4,"1000.00")
#     # vat_amount = get_tl_vfor_value(5, str(order_tax))#get_tl_vfor_value(5, "150.00")
#     # tagsbuff = comp+vat_num+order_date+tot_amount+vat_amount
#     # conv_bytes = bytes.fromhex(tagsbuff.hex())
#     # qrt1 = base64.b64encode(conv_bytes)
#     # qrt=str(qrt1.decode())
#     # print(qrt)
#     if action == 'order':
#             order.status = 'Prepared'
#             order.save()

#     if action == 'new_order':
#             order, created = Orders.objects.get_or_create(status = 'Started', created_by=request.user.username)
#             items = OrderItems.objects.filter(order_id=order.id)
#             order.save()

#     if action == 'Canceled':
#         if order.status == "Started":
#             items = OrderItems.objects.filter(order_id=order.id)
#             items.delete()
#             order.tax = 0
#             order.sub_total = 0
#             order.sub_total = 0
#             order.total_amount = 0
#             order.save()

#         else:

#             order.status = 'Canceled'
#             order.save()
#             items = None


#     action=request.GET.get('action')

#     if action == "submit":
#         order_type = request.GET.get('order_type')
#         order.order_type = order_type
#         order.status = 'Prepared'
#         order.save()

#     if action == 'Closed':
#         try:
#             for item in items:
#                 for ing in item.product_id.ingredients.all():
#                     ing.inventory.measurement -=ing.measurement * item.quantity
#                     ing.save()
#                     ing.inventory.save()

#                     item.product_id.save()
#         except:
#             pass

#         order.status = 'Closed'
#         order.save()
#         order_invoice, created = Orders.objects.get_or_create(order_id_id = order.id, created_by=request.user.username)

#     now = timezone.now()
#     now = timezone.localtime(now)
#     order.updated_date = now
#     order.save()


#     items = OrderItems.objects.filter(order_id=order.id)
#     order2 = Orders.objects.filter(created_by=request.user.username, status='Prepared')

#     try:
#         product = Products.objects.get(id=pid)
#         if product.Category_id.is_parent == True:
#             current_parent_cate=product.Category_id
#         else:
#             parent_name = product.Category_id.parent
#             current_parent_cate=Categories.objects.get(name=parent_name)

#         child_categories = Categories.objects.filter(pos= True, digital_menu =True, is_parent =False, parent=current_parent_cate.name).all()
#         products = Products.objects.filter(Q(Category_id__parent=current_parent_cate.name) | Q(Category_id=current_parent_cate) , pos=True).all()


#         # if order item not exist create new if it exists get it
#         order_item , created = OrderItems.objects.get_or_create(product_id= product, order= order)
#         order_item.name = product.name
#         name='Order #'+ str(order.id)

#         order_item.unit_price =product.total_amount

#         order_item.save()

#         if product.include_tax == 1:
#             total_price = product.selling_price + product.tax
#         else:
#             total_price = product.selling_price

#         # set Quntity
#         if action == 'add':
#             order_item.quantity += 1

#             order_item.save()
#         elif action == 'delete':
#             order_item.quantity -= 1
#             order_item.save()

#         order_item.save()
#         if order_item.quantity <= 0:
#             order_item.delete()

#         # get items of order
#         items = OrderItems.objects.filter(order_id=order.id)

#         for item in items:
#             if item.product_id.discount > 0 :
#                 net_price += (item.product_id.total_amount * item.quantity)
#                 discount = net_price * item.product_id.discount/100
#                 sub_total = net_price
#                 sub_total -= discount
#                 tax += item.product_id.tax * item.quantity
#                 if item.product_id.include_tax == True:
#                     sub_total -= tax
#                 else:
#                     item.product_id.total_amount += Decimal(0.15) * Decimal(item.product_id.selling_price)
#                     item.product_id.include_tax = True
#                     item.product_id.save()

#             else:
#                 net_price += (item.product_id.total_amount * item.quantity)
#                 sub_total = net_price

#                 tax += item.product_id.tax * item.quantity
#                 if item.product_id.include_tax == True:
#                     sub_total -= tax
#                 else:
#                     item.product_id.total_amount += Decimal(0.15) * Decimal(item.product_id.selling_price)
#                     item.product_id.include_tax = True
#                     item.product_id.save()

#         if product.include_tax == 1:
#             total += net_price - discount

#         else:
#             total += sub_total
#             total += tax

#         order.tax = tax
#         order.total_amount = total
#         order.name =name
#         order.sub_total = sub_total
#         order.total_discount = discount
#         order.created_by = request.user.username

#         now = timezone.now()
#         order.updated_date = now
#         order.save()

#     except Product.DoesNotExist:
#         product = None

#     context ={
#         'products': products,
#         'parent_categories': parent_categories,
#         'child_categories': child_categories,
#         'items': items,
#         'order':order,
#         'total': total,
#         'discount':discount,
#         'sub_total': sub_total,
#         'tax':tax,
#         'total_price':total_price,
#         'order2':order2,
#         'qrt':qrt,
#     }

#     return render(request, 'pos2.html', context)
