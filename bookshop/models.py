from django.db import models

# Create your models here.

CUSTOMER_STATUS = ((0, "Active"), (1, "Archived"), (2, "Suspended"))
BOOK_AVAILABILITY = ((0, "Unavailable"), (1, "Available"))
# Define the genre choices
AUTOBIOGRAPHY = 'Autobiography'
FANTASY = 'Fantasy'
CHILDRENS = "Children's"
MYSTERY = 'Mystery'
TRASHY = 'Trashy'
DRAMA = 'Drama'
HUMOR = 'Humor'
SCI_FI = 'Science Fiction'
NON_FICTION = 'Non-Fiction'
POLITICAL_MEMOIR = 'Political memoir'
HISTORICAL = 'Historical'
SATIRE = 'Satire'
VAUDEVILLE = 'Vaudeville'
BIOGRAPHY = 'Biography'
POETRY = 'Poetry'
HORROR = 'Horror'
SPORTS = 'Sports'
FICTION = 'Fiction'

BOOK_GENRE_CHOICES = (
    (AUTOBIOGRAPHY, 'Autobiography'),
    (FANTASY, 'Fantasy'),
    (CHILDRENS, "Children's"),
    (MYSTERY, 'Mystery'),
    (TRASHY, 'Trashy'),
    (DRAMA, 'Drama'),
    (HUMOR, 'Humor'),
    (SCI_FI, 'Science Fiction'),
    (NON_FICTION, 'Non-Fiction'),
    (POLITICAL_MEMOIR, 'Political memoir'),
    (HISTORICAL, 'Historical'),
    (SATIRE, 'Satire'),
    (VAUDEVILLE, 'Vaudeville'),
    (BIOGRAPHY, 'Biography'),
    (POETRY, 'Poetry'),
    (HORROR, 'Horror'),
    (SPORTS, 'Sports'),
    (FICTION, 'Fiction')
)

class Customer(models.Model):
    first_name = models.CharField(max_length=20)  
    last_name = models.CharField(max_length=20)  
    email = models.EmailField(max_length=60)
    status = models.IntegerField(choices=CUSTOMER_STATUS, default=0)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    books = models.ManyToManyField("Book", through="OrderItem", related_name="orders")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey("Book", on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "book"], name="unique_book_per_order"),
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="quantity_at_least_one"),
        ]

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=40)
    genre = models.CharField(max_length=40, choices=BOOK_GENRE_CHOICES)
    pages = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    availability = models.IntegerField(choices=BOOK_AVAILABILITY, default=1)
