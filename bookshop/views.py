import csv
from django.db.models import F, IntegerField, Sum, Value
from django.db.models.functions import Coalesce, Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
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

def get_customer_data(request, customer_id):
    customer_queryset = Customer.objects.filter(pk=customer_id)
    orders_queryset = OrderItem.objects.filter(order__customer_id=customer_id)

    customer = serializers.serialize("json", customer_queryset)
    orders = serializers.serialize("json", orders_queryset)

    return JsonResponse([customer, orders], safe=False)

def view_customer(request, customer_id):
    customer = get_object_or_404(request, customer_id)

    return render(
        request,
        "bookshop/customer.html",
        {
            "customer": customer,
        }
    )

def get_all_transformed_orders(request):
    transformed_data = (
        Order.objects.filter(customer__status="ACTIVE")
        .prefetch_related('customer')
        .annotate(
            customer_name=Concat('customer__first_name', Value(" "), 'customer__last_name'),
            customer_email=F('customer__email'),
            total=Coalesce(
                Sum(F("items__quantity") * F("items__book__price"), output_field=IntegerField()),
                0,
            ),
        )
    ).values_list('pk', 'customer__id', 'customer_name', 'customer_email', 'total')

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="transformed_order_data.csv"'},
    )
    
    writer = csv.writer(response)
    writer.writerow(['order_id', 'customer_id', 'customer_name', 'customer_email','total'])
    writer.writerows(transformed_data)

    return response
