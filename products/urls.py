from django.urls import path
from . import views
from .apps import ProductsConfig


app_name = ProductsConfig.name

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
]
