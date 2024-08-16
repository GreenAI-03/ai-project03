from .models import Category, Product, Sale, OrderItem, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, BarcodeForm
from django.http import JsonResponse
import json

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'pos_system/index.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'pos_system/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'pos_system/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



def checkout(request):
    if request.method == 'POST':
        cart_items = request.POST.getlist('cart_items')
        order = Order.objects.create(user=request.user)

        for item_id in cart_items:
            product = Product.objects.get(id=item_id)
            OrderItem.objects.create(order=order, product=product, quantity=1)

        return redirect('success_page')  # 重定向到一个成功页面
    return render(request, 'checkout.html')


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    product = Product.objects.get(id=product_id)
    
    cart = request.session.get('cart', {})
    
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
        }
    
    request.session['cart'] = cart
    
    return redirect('index')


import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from .models import Sale
from django.db.models import Sum
from datetime import timedelta, datetime

def get_sales_data(time_delta):
    now = datetime.now()
    start_date = now - time_delta
    sales = Sale.objects.filter(sale_date__gte=start_date)
    return sales

def sales_chart(request, period):
    if period == 'Daily':
        delta = timedelta(days=1)
    elif period == 'weekly':
        delta = timedelta(weeks=1)
    elif period == 'monthly':
        delta = timedelta(weeks=4)
    elif period == 'quarterly':
        delta = timedelta(weeks=13)
    elif period == 'semiannually':
        delta = timedelta(weeks=26)
    elif period == 'yearly':
        delta = timedelta(weeks=52)
    else:
        delta = timedelta(days=1)
    
    sales = get_sales_data(delta)
    dates = sales.values_list('sale_date', flat=True)
    totals = sales.values_list('quantity', flat=True)
    
    plt.figure(figsize=(10,6))
    plt.plot(dates, totals)
    plt.title(f'{period.capitalize()} Sales Analysis')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'sales_chart.html', {'graphic': graphic})



from django.shortcuts import render
from .forms import BarcodeForm

def barcode_scanner(request):
    if request.method == 'POST':
        form = BarcodeForm(request.POST)
        if form.is_valid():
            # 获取用户输入的条码
            barcode = form.cleaned_data['barcode']
            # 在这里处理条码，例如查询数据库或调用API
            result = process_barcode(barcode)  # 假设有一个函数处理条码
            return render(request, 'barcode_scanner.html', {'form': form, 'result': result})
    else:
        form = BarcodeForm()
    return render(request, 'barcode_scanner.html', {'form': form})

from .models import Sale, Product, Customer, Purchase

def process_barcode(barcode):
    # 这是一个简单的示例，实际功能可能包括数据库查询或API调用
    if barcode == " ":
        return "Customer Name: , Price: $10.00"
    else:
        return "No product found for this barcode."


