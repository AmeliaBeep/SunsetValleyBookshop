from django.db.models import CharField, F, IntegerField, Sum, Value
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

    transformed_customers = customers.annotate(name=Concat(
        "first_name", 
        Value(" "), 
        "last_name", 
        output_field=CharField())
    ).values_list('pk', 'name', 'email','status')
    
    print(transformed_customers)
    

    return render(
        request,
        "bookshop/orders.html",
        {
            "transformed_customers": transformed_customers,
        },
    )
