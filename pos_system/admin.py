from django.contrib import admin
from .models import Category, Product, Sale

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # 顯示的額外行數

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ProductInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description')


from django.contrib import admin
from .models import Sale  # 確保導入您的模型

class SaleAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'unit_price', 'sale_date', 'total_price')
    list_filter = ('sale_date',)
    search_fields = ('product_name',)

admin.site.register(Sale, SaleAdmin)




