from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('statistics/', views.statistics_view, name='statistics'),  # 新增統計頁面
    path('get-chart-data/', views.get_chart_data, name='get_chart_data'),
]
