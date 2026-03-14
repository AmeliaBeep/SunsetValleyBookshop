from django.shortcuts import get_object_or_404, render
from bookshop.models import Customer, Order

# Create your views here.

def view_orders(request):

    order_list = Order.objects.all()

    return render(
        request,
        "bookshop/orders.html",
        {
            "questions": order_list,
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

