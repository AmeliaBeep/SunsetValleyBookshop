from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name='home'),
    path('get-customer/<int:customer_id>', views.get_customer, name='get_customer'),
    path('view-customer/<int:customer_id>', views.view_customer, name='view_customer'),
    path('get-all-transformed-orders', views.get_all_transformed_orders, name='get_all_transformed_orders')
]