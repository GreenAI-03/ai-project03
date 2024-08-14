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
    list_display = ('product_class', 'product_name', 'quantity', 'unit_price', 'sale_date', 'total_price', )
    list_filter = ('sale_date', 'product_class', 'product_name', ) 
    search_fields = ('product_name', 'sale_date', 'product_class',  'unit_price',)
    
admin.site.register(Sale, SaleAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'e_invoice_carrier', 'created_at')
    search_fields = ('e_invoice_carrier', 'name', 'email', 'phone_number')
    list_filter = ('created_at','phone_number', 'e_invoice_carrier',)

admin.site.register(Customer, CustomerAdmin)