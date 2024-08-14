from .models import Category, Product, Sale
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import JsonResponse

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    categories = Category.objects.all()
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
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

import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Sale, OrderItem, Order

# ！！！！有問題！！！！
# 點擊結帳後導向有問題
def checkout(request):
    if request.method == 'POST':
        cart_items = request.POST.getlist('cart_items')
        order = Order.objects.create(user=request.user)

        for item_id in cart_items:
            product = Product.objects.get(id=item_id)
            OrderItem.objects.create(order=order, product=product, quantity=1)

        return redirect('success_page')  # 重定向到一个成功页面
    return render(request, 'checkout.html')


# add_to_cart函數
# ！！！！有問題！！！！
# 購屋車不會顯示 系統回應Not Found: /add-to-cart/
from django.http import JsonResponse
from .models import Product
from django.shortcuts import get_object_or_404

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        
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
        
        return JsonResponse({'cart': cart})
