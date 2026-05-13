import csv
from django.db.models import F, IntegerField, Sum, Value
from django.db.models.functions import Coalesce, Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from bookshop.forms import OrderForm, OrderItemForm
from bookshop.models import Customer, Order, OrderItem
from django.core import serializers
from django.urls import reverse_lazy

# Create your views here.

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
class CustomerListView(ListView):
    model = Customer
    template_name = "bookshop/customer_list"
    context_object_name = "customers"
    paginate_by = 20


class CustomerDetailView(DetailView):
    model = Customer
    template_name = "bookshop/customer.html"
    context_object_name = "customer"
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context["orders"] = (
            Order.objects.filter(customer=self.object.pk)
            .prefetch_related("items__book")
        )
        return context  


class OrderCreateView(View):
    order_form = OrderForm()
    order_item_form = OrderItemForm()
    template_name = "bookshop/order_create.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "order_form": self.order_form,
                "order_item_form": self.order_item_form,
            },
        )







# OrderUpdateView

# OrderDeleteView