from django.contrib import admin
from .models import Category, Product, Sale, Customer

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
    
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product_category', 'product', 'quantity', 'unit_price', 'sale_date', 'total_price', )
    list_filter = ('sale_date', 'product_category', 'product', ) 
    search_fields = ('product', 'sale_date', 'product_category',  'unit_price',)
    
admin.site.register(Sale, SaleAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'email', 'phone_number', 'phone_barcode', 'created_at', 'birthday')
    search_fields = ('phone_barcode', 'customer_name', 'email', 'phone_number', 'birthday')
    list_filter = ('created_at','phone_number', 'phone_barcode', 'birthday')

admin.site.register(Customer, CustomerAdmin)