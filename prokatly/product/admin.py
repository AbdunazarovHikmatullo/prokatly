from django.contrib import admin
from .models import Category, Product, ProductImage, Rental , Favorite

# === Категории ===
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)     # ✅ добавил
    list_filter = ("parent",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)



class ProductImageInline(admin.TabularInline):  
    model = ProductImage
    extra = 1  # сколько пустых форм для загрузки будет показываться
    fields = ("image", "is_main")
    readonly_fields = ("uploaded_at",)
    show_change_link = True



# === Товары ===
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "owner", "category",
        "price", "price_period", "is_available","available_status",
        "is_price_negotiable", "is_vip", "status", "created_at"
    )
    list_filter = ("status", "is_available", "is_vip", "category", "price_period")
    search_fields = ("title", "desc", "owner__phone_number")  # ✅ уже есть
    autocomplete_fields = ("owner", "category")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_editable = ("status", "is_available", "is_vip")
    date_hierarchy = "created_at"

    inlines = [ProductImageInline]

# === Аренды ===
@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "start_day", "end_day", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__phone_number", "product__title")  # ✅ уже есть
    autocomplete_fields = ("user", "product")
    ordering = ("-created_at",)
    date_hierarchy = "start_day"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display =['product', 'created_at']