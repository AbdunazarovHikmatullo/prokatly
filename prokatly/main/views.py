from django.shortcuts import render
from product.models import Product, Category


def index(request):
    products = Product.objects.order_by('-is_vip')
    categories = Category.objects.filter(parent=None)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'main/index.html', context)