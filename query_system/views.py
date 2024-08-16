from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from pos_system.models import Customer

def customer_info(request, phone_barcode):
    # 根據手機條碼查找顧客
    customer = get_object_or_404(Customer, phone_barcode=phone_barcode)
    
    # 準備要返回的資料
    customer_data = {
        'customer_name': customer.customer_name,
        'email': customer.email,
        'birthday': customer.birthday,
        'phone_number': customer.phone_number,
        'address': customer.address,
        'phone_barcode': customer.phone_barcode,
        'special_requests': customer.special_requests,
        'created_at': customer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': customer.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    return JsonResponse(customer_data)
