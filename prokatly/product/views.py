from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateProductForm, ProductImageFormSet
from .models import Product
def create_product(request):
    if request.method == "POST":
        form = CreateProductForm(request.POST)
        formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            formset.instance = product
            formset.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = CreateProductForm()
        formset = ProductImageFormSet()

    return render(request, "product/create_product.html", {
        "form": form,
        "formset": formset
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    context ={
        'product':product
    }
    return render(request, 'product/detail.html', context)



def product_list(request):
    return render(request, 'product/product-list.html')