from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import F, Sum
from django.utils.timezone import make_aware
from decimal import Decimal
from itertools import combinations
from collections import Counter
import datetime
import json

from .models import Category, Product, Sale, Order, OrderItem
from .forms import CustomUserCreationForm


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


@require_POST
@transaction.atomic
def checkout(request):
    now = timezone.localtime(timezone.now())
    print(f"Checkout time: {now}")  # 输出結帳時間到控制台
    try:
        cart = request.session.get('cart', {})
        
        if not cart:
            return JsonResponse({'success': False, 'error': '購物車是空的'})

        # 将当前时间转换为台湾时区并设置为订单创建时间
        now = timezone.localtime(timezone.now())
        order = Order.objects.create(user=request.user, created_at=now)

        total_amount = Decimal('0.00')

        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            price = Decimal(str(item['price']))

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

            Sale.objects.create(
                product=product,
                quantity=quantity,
                sale_date=order.created_at  # 使用已確認的時區感知时间
            )

            total_amount += price * quantity

        request.session['cart'] = {}
        request.session.modified = True
        
        return JsonResponse({'success': True, 'message': '結帳成功', 'order_id': order.id})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': '商品不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

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


def statistics_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # 計算日營收
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)

    # 確保 start_of_week 和 end_of_week 是時區感知的 datetime
    start_of_week = make_aware(datetime.datetime.combine(start_of_week, datetime.time.min))
    end_of_week = make_aware(datetime.datetime.combine(end_of_week, datetime.time.max))

    # 使用 aggregation 方法來計算總營收
    sales_today = Sale.objects.filter(sale_date__date=today)
    daily_revenue = sales_today.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or 0

    # 計算每週熱門商品
    weekly_sales = Sale.objects.filter(sale_date__range=[start_of_week, end_of_week])
    most_popular_products = weekly_sales.values('product__name').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')

    # 計算每週不熱門商品
    least_popular_products = weekly_sales.values('product__name').annotate(
        total_quantity=Sum('quantity')
    ).order_by('total_quantity')

    context = {
        'daily_revenue': daily_revenue,
        'most_popular_products': most_popular_products,
        'least_popular_products': least_popular_products,
    }
    
    return render(request, 'pos_system/statistics.html', context)


def get_chart_data(request):
    today = timezone.now().date()
    week_ago = today - datetime.timedelta(days=7)

    revenue_data = []
    revenue_labels = []
    
    for i in range(7):
        day = week_ago + datetime.timedelta(days=i)
        # 确保日期是時區感知的的 datetime
        start_of_day = make_aware(datetime.datetime.combine(day, datetime.time.min))
        end_of_day = make_aware(datetime.datetime.combine(day, datetime.time.max))
        
        # 計算每天總營收
        total_revenue = Sale.objects.filter(sale_date__range=[start_of_day, end_of_day]).aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or Decimal('0.00')
        
        revenue_data.append(float(total_revenue))  # 轉換為 float 類型以符合前端
        revenue_labels.append(day.strftime('%Y-%m-%d'))

    popular_sales = Sale.objects.filter(sale_date__gte=week_ago).values('product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    popular_products_labels = [sale['product__name'] for sale in popular_sales]
    popular_products_data = [sale['total_quantity'] for sale in popular_sales]

    unpopular_sales = Sale.objects.filter(sale_date__gte=week_ago).values('product__name').annotate(total_quantity=Sum('quantity')).order_by('total_quantity')[:5]
    unpopular_products_labels = [sale['product__name'] for sale in unpopular_sales]
    unpopular_products_data = [sale['total_quantity'] for sale in unpopular_sales]

    all_combinations = []
    for order in Order.objects.filter(created_at__gte=week_ago):
        items = OrderItem.objects.filter(order=order).values_list('product__name', flat=True)
        for r in range(2, len(items) + 1):
            combs = combinations(sorted(items), r)
            all_combinations.extend(combs)

    combination_counts = Counter(all_combinations)
    most_common_combinations = combination_counts.most_common(5)

    best_combinations_labels = [' & '.join(comb) for comb, _ in most_common_combinations]
    best_combinations_data = [count for _, count in most_common_combinations]

    return JsonResponse({
        'revenue_labels': revenue_labels,
        'revenue_data': revenue_data,
        'popular_products_labels': popular_products_labels,
        'popular_products_data': popular_products_data,
        'unpopular_products_labels': unpopular_products_labels,
        'unpopular_products_data': unpopular_products_data,
        'best_combinations_labels': best_combinations_labels,
        'best_combinations_data': best_combinations_data,
    })
