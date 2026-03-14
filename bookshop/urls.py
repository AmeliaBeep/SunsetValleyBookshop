from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_orders, name='view_orders'),
    path('view-customer/<int:customer_id>', views.view_customer_data, name='view_customer_data'),
    path('get-all-order-totals')
]