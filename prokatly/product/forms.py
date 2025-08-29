from django import forms
from django.forms import inlineformset_factory
from .models import Product, Category, ProductImage


class CreateProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Категория"
    )

    class Meta:
        model = Product
        fields = [
            'title',
            'desc',
            'price',
            'price_period',
            'is_price_negotiable',
            'location',
            'is_available',
            'available_status',
            'status',
            'is_vip',
            'category',
        ]
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']


ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,               # по умолчанию 3 поля для загрузки
    can_delete=True
)
