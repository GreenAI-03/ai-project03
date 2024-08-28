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
    path('upload-menu/', views.upload_menu, name='upload_menu'), #菜單上傳
    path('save-menu-items/', views.save_menu_items, name='save_menu_items'), #菜單上傳  
    path('uncategorized-items/', views.uncategorized_items, name='uncategorized_items'),
    path('move-item/<int:item_id>/', views.move_item, name='move_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('update-price/<int:item_id>/', views.update_price, name='update_price'),
]
