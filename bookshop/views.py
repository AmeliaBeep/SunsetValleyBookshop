from django.db.models import CharField, F, IntegerField, Sum, Value, Prefetch
from django.db.models.functions import Coalesce, Concat
from django.shortcuts import get_object_or_404, render
from bookshop.models import Customer, Order


# Create your views here.

def view_orders(request):

    order_list = Order.objects.all()

    return render(
        request,
        "bookshop/orders.html",
        {
            "order_list": order_list,
        },
    )

def view_customer_data(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    return render(
        request,
        "bookshop/customer.html",
        {
            "customer": customer,
        }
    )

def get_all_transformed_orders(request):
    customers=Customer.objects.filter(status='ACTIVE')


    

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
    ).values('pk', 'customer__id', 'customer_name', 'customer_email', 'total')

    return render(
        request,
        "bookshop/orders.html",
        {
            "transformed_customers": transformed_data,
        },
    )
