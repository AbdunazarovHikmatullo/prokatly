from django.db import models
from account.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Родительская категория")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['parent', 'name'], name='unique_category_per_parent')
        ]

    
    def __str__(self):
        if self.parent:
            return f"{self.parent} → {self.name}"
        return self.name

    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)




class Product(models.Model):
    PRICE_PERIOD_CHOICES = [
        ('day', 'День'),
        ('week', 'Неделя'),
        ('month', 'Месяц'),
        ('year', 'Год'),
    ]
    STATUS_CHOICES = [
        ('moderation', 'В модерации'),
        ('available', 'Доступен'),
        ('banned', 'Забанен'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('available', 'Доступен'),
        ('low_stock', 'Осталось мало'),
        ('unavailable', 'Недоступен'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="products")
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    price_period = models.CharField(max_length=10, choices=PRICE_PERIOD_CHOICES, default='day', verbose_name="Период аренды")
    is_price_negotiable = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    available_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available', verbose_name='Статус доступности')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='moderation')
    is_vip = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="products",verbose_name="Категория")
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def display_availability(self):
        if not self.is_available:
            return 'Скрыт'
        return dict(self.AVAILABILITY_CHOICES).get(self.available_status, 'Доступен')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return f"{self.owner.phone_number} - товар {self.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by', verbose_name="Товар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные товары"
        unique_together = ('user', 'product')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Товар"
    )
    image = models.ImageField(
        upload_to="product/images/%Y/%m/%d/",
        verbose_name="Изображение"
    )
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ["-is_main", "id"]  # главная картинка всегда первая
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Изображение {self.product.title}"




class Rental(models.Model):
    STATUS_CHOICE = [
        ('active', 'Активна'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="rentals")
    start_day = models.DateField()
    end_day = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.phone_number} - {self.product.title}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
