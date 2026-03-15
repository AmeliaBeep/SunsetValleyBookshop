import csv
from django.db.models import F, IntegerField, Sum, Value
from django.db.models.functions import Coalesce, Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from bookshop.models import Customer, Order, OrderItem
from django.core import serializers

# Create your views here.

def view_home(request):

    customer_list = Customer.objects.all()

    return render(
        request,
        "bookshop/home.html",
        {
            "customers": customer_list,
        },
    )


class CustomerLookupMixin:
    def get_customer(self, customer_id):
        return get_object_or_404(Customer, pk=customer_id)


class CustomerDataView(CustomerLookupMixin, View):
    def get(self, request, customer_id):
        customer = self.get_customer(customer_id)
        orders = (
            Order.objects
            .filter(customer_id=customer_id)
            .select_related("customer")
            .prefetch_related("items__book")
        )

        data = {
            "customer": {
                "id": customer.pk,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "status": customer.status,
            },
            "orders": {
                str(order.pk): {
                    "order_id": order.pk,
                    "order_items": {
                        str(item.pk): {
                            "book_id": item.book_id,
                            "book_title": item.book.title,
                            "quantity": item.quantity,
                            "unit_price": item.book.price,
                            "line_total": item.quantity * item.book.price,
                        }
                        for item in order.items.all()
                    },
                }
                for order in orders
            },
        }
        return JsonResponse(data)


class CustomerDetailView(CustomerLookupMixin, View):
    template_name = "bookshop/customer.html"

    def get(self, request, customer_id):
        customer = self.get_customer(customer_id)
        return render(
            request, 
            self.template_name, 
            {
                "customer": customer
            },
        )
