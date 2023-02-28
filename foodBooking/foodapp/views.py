from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Restaurant, Menu, Order
from .serializers import RestaurantSerializer, MenuSerializer, OrderSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
