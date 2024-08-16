from django.db import models
import uuid
from django.contrib.auth.models import User
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0) # 新增價格欄位


    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    birthday = models.CharField(max_length=15, unique=False)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    customer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    special_requests = models.TextField(blank=True, null=True)
    phone_barcode = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.phone_barcode}"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cashier = models.CharField(max_length=100)
    special_requests = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales")
    
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
    
from django.db import models
from decimal import Decimal

class Purchase(models.Model):
    purchase_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def product_list(self):
        # 列出購買的產品明細
        return {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
        }

    def __str__(self):
        return f"Purchase {self.customer.customer_name} - {self.product.name} - {self.total_price} on {self.purchase_date}"


