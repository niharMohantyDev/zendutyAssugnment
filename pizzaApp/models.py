from django.db import models

# Create your models here.

class PizzaBase(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cheese(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Topping(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Pizza(models.Model):
    base = models.ForeignKey(PizzaBase, on_delete=models.CASCADE)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)

class Order(models.Model):
    pizzas = models.ManyToManyField(Pizza)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Placed')
