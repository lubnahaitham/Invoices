from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Setting, Invoice, Product


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['supplier_name', 'supplier_site', 'vat_registratoion_number', 'attention',
                  'reference_number', 'reference_number_one', 'telephone_number', 'branch', 'attention_one']

  

    labels = {
        'supplier_name': 'Supplier Name',
        'supplier_site': 'Supplier Site',
        'vat_registratoion_number': 'Vat Registration Number',
        'attention': 'Attention',
        'reference_number': 'Reference Number',
        'telephone_number': 'Telephone Number',
    }



class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'invoice_issue_date']
#         fields = ['date_of_supply', 'branch', 'salesman_name', 'invoice_number',
#                   'invoice_issue_date', 'page_number', 'quantity', 'buyer_organization_name', 'building_number', 
#                   'street_name', 'district', 'city', 'country', 'postal_code', 'additional_number', 'vat_number', 'other_buyer_id']
                #   'unit_price', 'quantity', 'discount', 
                #   'taxable_amount', 'tax_amount', 'tax_rate', 'total_vat', 'total_taxable_amount_exclude_vat',
                #   'total_exclude_vat', 'total_amount_due', 'sub_total'

    labels = {
    #     'date_of_supply': 'Date Of Supply',
    #     'branch': 'Branch',
    #     'salesman_name': 'Sales Man Name',
        'invoice_number': 'Invoice Number',
        'invoice_issue_date': 'Invoice Issue Date',
    #     'page_number': 'Page Number',

    #     'buyer_organization_name': 'Organization Name',
    #     'building_number': 'Building Number',
    #     'street_name': 'Street Name',
    #     'district': 'District',
    #     'city': 'City',
    #     'country': 'Country',
    #     'postal_code': 'Postal Code',
    #     'additional_number': 'Additional Number',
    #     'vat_number': 'Vat Number',
    #     'other_buyer_id': 'Other Buyer Id',

    
        # 'unit_price': 'Price',
        # 'quantity': 'Quantity',
        # 'discount': 'Discount',
        # 'taxable_amount': 'Taxable Amount',
        # 'tax_amount': 'Tax Amount',
        # 'tax_rate': 'Tax Rate',
        # 'total_vat': 'Total Vat',
        # 'total_taxable_amount_exclude_vat': 'Total Taxable Amount Exclude Vat',
        # 'total_exclude_vat': 'Total exclude Vat',
        # 'total_amount_due': 'Total Amount Due',
        # 'sub_total': 'Sub-Total'

    }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_code', 'note', 'uom', 'item_name', 'item_name_in_arabic', 'price']

    labels = {
        'item_code': 'Item Code',
        'item_name': 'Item Name',
        'note': 'Note',
        'uom': 'UOM',
        'item_name_in_arabic': 'Item Name In Arabic',
        'price': 'Price'
    }
    

