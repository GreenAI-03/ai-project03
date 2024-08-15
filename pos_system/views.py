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
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Order, OrderItem, Product
from decimal import Decimal

@require_POST
@transaction.atomic
def checkout(request):
    try:
        # 获取当前购物车
        cart = request.session.get('cart', {})
        
        if not cart:
            return JsonResponse({'success': False, 'error': '購物車是空的'})

        # 创建订单
        order = Order.objects.create(user=request.user)

        total_amount = Decimal('0.00')

        # 将购物车商品转换为订单项
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            price = Decimal(str(item['price']))  # 确保价格是 Decimal 类型

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

            total_amount += price * quantity

        # 可以在这里更新订单的总金额（如果 Order 模型有这个字段）
        # order.total_amount = total_amount
        # order.save()

        # 清空购物车
        request.session['cart'] = {}
        request.session.modified = True
        
        return JsonResponse({'success': True, 'message': '結帳成功', 'order_id': order.id})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': '商品不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
    
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def add_to_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        product_id = body_data.get('product_id')
        quantity = int(body_data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'name': product.name,
                'price': str(product.price),  # 将 Decimal 转换为字符串
                'quantity': quantity,
            }
        request.session['cart'] = cart

        return JsonResponse({'cart': cart})

