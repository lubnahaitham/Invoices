from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect

from .decorators import unauthenticated_user
from .forms import InvoiceFormset, SettingForm, ProductForm, CreateUserForm, InvoiceForm
from .models import Setting,Invoice, Product
from django.db.models import Q


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
    product_data = Product.objects.get(pk=id)
    invoice_data = Invoice.objects.get(pk=id)
    context = {'setting_data_view': Setting.objects.get(id=1),
               'invoice_data': invoice_data, 'product_data': product_data}
    return render(request, "pos/pos_view.html", context)


def invoice_create(request):
    setting_data = Setting.objects.get(id=1)
    # formset = InvoiceFormset(request.POST or None)
    invoice_form = InvoiceForm(request.POST or None)
    products = list(Product.objects.all())

    context = {
        "invoice_form": invoice_form,
        "setting_data": setting_data,
        "products": products,
    
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
