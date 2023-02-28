from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Restaurant, MenuItem, Order


@login_required
def restaurant_dashboard(request):
    restaurant = request.user.restaurant
    orders = Order.objects.filter(restaurant=restaurant).order_by('-date')
    order_count = orders.count()
    order_total = orders.aggregate(Sum('total'))['total__sum'] or 0
    context = {'restaurant': restaurant, 'orders': orders, 'order_count': order_count, 'order_total': order_total}
    return render(request, 'restaurant/dashboard.html', context)


@login_required
def create_menu(request):
    restaurant = request.user.restaurant
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        MenuItem.objects.create(restaurant=restaurant, name=name, description=description, price=price)
        return redirect('restaurant_dashboard')
    return render(request, 'restaurant/create_menu.html')


def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'menu.html', {'items': items})


@login_required
def order(request):
    items = MenuItem.objects.all()
    restaurant = request.user.restaurant
    if request.method == 'POST':
        order_items = []
        total = 0
        for item in items:
            quantity = request.POST.get(str(item.id))
            if quantity != '' and int(quantity) > 0:
                order_items.append((item, int(quantity)))
                total += item.price * int(quantity)
        if len(order_items) > 0:
            if Order.objects.filter(restaurant=restaurant).count() < 10:
                order = Order.objects.create(user=request.user, restaurant=restaurant, total=total)
                for item, quantity in order_items:
                    order.items.add(item)
                messages.success(request, 'Your order has been placed')
                return redirect('order_history')
            else:
                messages.error(request, 'This restaurant is not accepting orders at this time')
        else:
            messages.warning(request, 'You did not select any items')
    return render(request, 'order.html', {'items': items})


@login_required
def order_history(request):
    user = request.user
    restaurant = request.user.restaurant
    orders = Order.objects.filter(restaurant=restaurant) if restaurant else Order.objects.filter(user=user)
