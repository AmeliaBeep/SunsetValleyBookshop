import os
import django
from django.shortcuts import get_object_or_404
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from bookshop.models import Book, Customer, OrderItem, Order

fake = Faker()

# Clear any existing order data
#Order.objects.all().delete()

# Create 15 orders
customer_list = list(Customer.objects.all())
book_list = list(Book.objects.all())

for _ in range(15):  # create 15 orders
    order = Order.objects.create(
        customer=fake.random_element(elements=customer_list)
    )

    selected_books = fake.random_elements(
        elements=book_list,
        length=fake.random_int(min=1, max=min(4, len(book_list))),
        unique=True,
    )

    for book in selected_books:
        quantity = fake.random_int(min=1, max=3)
        OrderItem.objects.create(
            order=order,
            book=book,
            quantity=quantity,
        )

# order = get_object_or_404(Order, pk=3)
# for item in order.items.all():
#     print(f'Order {order.id} by {order.customer.first_name} {order.customer.last_name} totaled {order.total} and consisted of: {item.quantity} copies of {item.book.title} each costing {item.book.price}')
