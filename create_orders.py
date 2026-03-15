from bookshop.models import Book, Customer, OrderItem, Order
import os
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


fake = Faker()

# Create 20 orders
customer_list = list(Customer.objects.all())
book_list = list(Book.objects.all())

for _ in range(20):
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
