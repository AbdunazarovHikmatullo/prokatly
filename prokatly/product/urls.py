from django.urls import path
from .views import create_product, product_detail, product_list



urlpatterns = [
    path('create/', create_product, name='create_product'),
    path('detail/<int:id>/', product_detail, name='product_detail'),
    path('list/', product_list, name='product_list')
]