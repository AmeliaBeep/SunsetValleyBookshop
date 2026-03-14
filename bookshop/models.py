from django.db import models

# Create your models here.

STATUS = ((0, "Active"), (1, "Archived"), (2, "Suspended"))
GENRES = ((0, "Fiction"), (1, "Non-fiction"), (2, "Other"))

class Customer(models.Model):
    first_name = models.CharField(max_length=20)  
    last_name = models.CharField(max_length=20)  
    email = models.EmailField(max_length=30)
    status = models.IntegerField(choices=STATUS, default=0)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    books = models.ManyToManyField("Book", through="OrderItem", related_name="orders")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "book"], name="unique_book_per_order"),
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="quantity_at_least_one"),
        ]

class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    genre = models.IntegerField(choices=GENRES, default=0)
    price = models.IntegerField
