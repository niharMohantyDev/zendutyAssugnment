from celery import shared_task
from .models import Order
from datetime import datetime, timedelta,timezone

@shared_task
def update_order_status(order_id):
    try:
        order = Order.objects.get(id=order_id)
        elapsed_time = datetime.now(timezone.utc) - order.placed_at
        if elapsed_time.total_seconds() <= 60:
            order.status = 'Accepted'
        elif elapsed_time.total_seconds() <= 60 + 60:
            order.status = 'Preparing'
        elif elapsed_time.total_seconds() <= 60 + 60 + 180:
            order.status = 'Dispatched'
        elif elapsed_time.total_seconds() <= 60 + 60 + 180 + 300:
            order.status = 'Delivered'
        order.save()
    except Order.DoesNotExist:
        pass
