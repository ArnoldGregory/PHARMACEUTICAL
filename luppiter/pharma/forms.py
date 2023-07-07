from django import forms
from .models import Total_Customers, Medicine, Sale, Cart, Bill, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'


class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = Total_Customers
        fields = ['first_name', 'email',  'address']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Total_Customers
        fields = ['first_name', 'email',  'address']


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['pharmacist', 'medicine', 'quantity']


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantity', 'quantity')


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer', 'medicines']
        widgets = {
            'medicines': forms.CheckboxSelectMultiple
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'