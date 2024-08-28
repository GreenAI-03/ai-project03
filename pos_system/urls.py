from django.urls import path    
from . import views

urlpatterns = [
    path('', views.index, name='index'),  #首頁
    path('login/', views.login_view, name='login'),  #登入
    path('register/', views.register_view, name='register'),  #註冊
    path('logout/', views.logout_view, name='logout'),  #登出
    path('checkout/', views.checkout, name='checkout'),  #結帳
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),  #新增購物車
    path('statistics/', views.statistics_view, name='statistics'),  # 新增統計頁面
    path('get-chart-data/', views.get_chart_data, name='get_chart_data'),
    path('upload-menu/', views.upload_menu, name='upload_menu'), #菜單上傳
    path('save-menu-items/', views.save_menu_items, name='save_menu_items'), #菜單上傳  
    path('uncategorized-items/', views.uncategorized_items, name='uncategorized_items'),
    path('move-item/<int:item_id>/', views.move_item, name='move_item'),    #移動菜單
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),  #刪除菜單
    path('update-price/<int:item_id>/', views.update_price, name='update_price'),  #更新菜單價格
    path('history/', views.history_view, name='history'),   #歷史訂單
    path('order-details/<int:order_id>/', views.order_details, name='order_details'),   #訂單詳情
]
