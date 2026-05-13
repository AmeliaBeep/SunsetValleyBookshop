from django import forms

from .models import Customer, Order, OrderItem, Book

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer',)

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('book', 'quantity',)
