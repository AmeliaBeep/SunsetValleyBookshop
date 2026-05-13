from django.urls import path
from . import views

urlpatterns = [
     path("", views.CustomerListView.as_view(), name="customer_list_view"),
     path("customer-detail/<int:pk>",
         views.CustomerDetailView.as_view(), name="customer_detail_view"),
     path("create_order", views.OrderCreateView.as_view(), name="create_order_view")
]
