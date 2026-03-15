from django.contrib import admin

from bookshop.models import Book, Customer, Order, OrderItem

# Register your models here.

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
