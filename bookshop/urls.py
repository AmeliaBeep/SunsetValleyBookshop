from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_home, name="home"),
    path("get-customer/<int:customer_id>",
         views.CustomerDataView.as_view(), name="get_customer_data"),
    path("view-customer/<int:customer_id>",
         views.CustomerDetailView.as_view(), name="view_customer"),
]
