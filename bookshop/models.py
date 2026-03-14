from django.db import models

# Create your models here.

class Customer(models.Model):
    CUSTOMER_STATUS_CHOICES = (
        ('ACTIVE', 'Active'), 
        ('ARCHIVED', 'Archived'), 
        ('SUSPENDED', 'Suspended')
    )

    first_name = models.CharField(max_length=20)  
    last_name = models.CharField(max_length=20)  
    email = models.EmailField(max_length=60)
    status = models.CharField(max_length=20, choices=CUSTOMER_STATUS_CHOICES)


class Book(models.Model):
    BOOK_AVAILABILITY = (
        ('AVAILABLE', "Available"),
        ('UNAVAILABLE', 'Unavailable')
    ) 

    BOOK_GENRE_CHOICES = (
        ('AUTOBIOGRAPHY', 'Autobiography'),
        ('FANTASY', 'Fantasy'),
        ('CHILDRENS', "Children's"),
        ('MYSTERY', 'Mystery'),
        ('TRASHY', 'Trashy'),
        ('DRAMA', 'Drama'),
        ('HUMOR', 'Humor'),
        ('SCI_FI', 'Science Fiction'),
        ('NON_FICTION', 'Non-Fiction'),
        ('POLITICAL_MEMOIR', 'Political memoir'),
        ('HISTORICAL', 'Historical'),
        ('SATIRE', 'Satire'),
        ('VAUDEVILLE', 'Vaudeville'),
        ('BIOGRAPHY', 'Biography'),
        ('POETRY', 'Poetry'),
        ('HORROR', 'Horror'),
        ('SPORTS', 'Sports'),
        ('FICTION', 'Fiction')
    )

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=40)
    genre = models.CharField(max_length=40, choices=BOOK_GENRE_CHOICES)
    pages = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    availability = models.CharField(max_length=20, choices=BOOK_AVAILABILITY)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")
    books = models.ManyToManyField(Book, through="OrderItem", related_name="orders")
    total = models.PositiveIntegerField(default=0)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "book"], name="unique_book_per_order"),
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="quantity_at_least_one"),
        ]
