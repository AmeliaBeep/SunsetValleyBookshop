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
    
    def build_customer_payload(self, customer_id):
        customer = self.get_customer(customer_id)
        payload = {
            "id": customer.pk,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "status": customer.status,
        }
        return payload
    
    def build_orders_payload(self, customer_id):
        orders = (
            Order.objects
            .filter(customer_id=customer_id)
            .select_related("customer")
            .prefetch_related("items__book")
        )

        payload = {}
        for order in orders:
            order_items = {
                str(item.pk): {
                    "book_id": item.book_id,
                    "book_title": item.book.title,
                    "quantity": item.quantity,
                    "unit_price": item.book.price,
                    "line_total": item.quantity * item.book.price,
                }
                for item in order.items.all()
            }

            payload[str(order.pk)] = {
                "order_id": order.pk,
                "total": sum(item["line_total"] for item in order_items.values()),
                "order_items": order_items,
            }

        return payload  


class CustomerDataView(CustomerLookupMixin, View):
    def get(self, request, customer_id):
        customer = self.build_customer_payload(customer_id)
        orders = self.build_orders_payload(customer_id)
        data = {
            "customer": customer,
            "orders": orders,
        }
        return JsonResponse(data)


class CustomerDetailView(CustomerLookupMixin, View):
    template_name = "bookshop/customer.html"

    def get(self, request, customer_id):
        customer = self.get_customer(customer_id)
        orders = self.build_orders_payload(customer_id)
        return render(
            request,
            self.template_name,
            {
                "customer": customer,
                "orders": orders,
            },
        )
