from django.urls import path
from .views import *

urlpatterns = [
    path('orderpizza/', add_pizza_to_order),
    path('trackOrderStatus/<int:order_id>/', track_order_status),
]
