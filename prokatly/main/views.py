from django.shortcuts import render
from product.models import Product, Category


def index(request):
    products = Product.objects.filter(is_available=True, available_status='available', status='available').order_by('-is_vip','-created_at')
    categories = Category.objects.filter(parent=None)

    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'main/index.html', context)