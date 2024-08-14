from django.db import models
import uuid
from django.contrib.auth.models import User

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
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    birthday = models.CharField(max_length=15, unique=False)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    e_invoice_carrier = models.CharField(max_length=50, unique=True, blank=True, null=True)  # 電子載具
    customer_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # 顧客編號
    special_requests = models.TextField(blank=True, null=True)  # 特殊需求

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Sale(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    product_class = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cashier = models.CharField(max_length=100)  # 結帳人員
    invoice_number = models.CharField(max_length=100, unique=True)  # 發票號碼
    special_requests = models.TextField(blank=True, null=True)  # 顧客特殊需求
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales")
    
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product_name} - {self.quantity} units"
