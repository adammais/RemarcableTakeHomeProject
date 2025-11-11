from django.urls import path
from . import views

urlpatterns = [
    # Home page - shows product list with search and filter
    path('', views.product_list, name='product_list'),
]

