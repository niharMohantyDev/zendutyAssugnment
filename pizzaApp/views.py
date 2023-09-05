from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .tasks import update_order_status
from datetime import timezone
import datetime

@api_view(['POST'])
def add_pizza_to_order(request):
    if 'base' not in request.data or 'cheese' not in request.data or 'toppings' not in request.data:
        return Response({'message': 'Incomplete pizza data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        base_id = request.data['base']
        cheese_id = request.data['cheese']
        topping_ids = request.data['toppings']

        base = PizzaBase.objects.get(pk=base_id)
        cheese = Cheese.objects.get(pk=cheese_id)
        toppings = Topping.objects.filter(pk__in=topping_ids)

        pizza_price = base.price + cheese.price + sum(t.price for t in toppings)

        pizza = Pizza.objects.create(base=base, cheese=cheese)
        pizza.toppings.set(toppings)

        order = Order.objects.create(total_price=pizza_price, status='Placed')
        order.pizzas.add(pizza)

        if order.total_price is None:
            order.total_price = 0
        order.total_price += pizza_price
        order.save()

        return Response({'message': 'Pizza added to order', 'order_id': order.id}, status=status.HTTP_201_CREATED)

    except (PizzaBase.DoesNotExist, Cheese.DoesNotExist):
        return Response({'message': 'Invalid pizza base or cheese'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def track_order_status(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        elapsed_time = (datetime.datetime.now(timezone.utc) - order.placed_at).total_seconds()

        if elapsed_time <= 60:
            order.status = 'Accepted'
        elif elapsed_time <= 60 + 60:
            order.status = 'Preparing'
        elif elapsed_time <= 60 + 60 + 180:
            order.status = 'Dispatched'
        elif elapsed_time <= 60 + 60 + 180 + 300:
            order.status = 'Delivered'
        order.save()

        update_order_status.delay(order_id)

        return Response({'order_id': order.id, 'status': order.status}, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
