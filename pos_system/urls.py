from django.urls import path
from . import views
from .views import barcode_scanner

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('sales/<str:period>/', views.sales_chart, name='sales_chart'),
    path('scan/', barcode_scanner, name='barcode_scanner'),
]
