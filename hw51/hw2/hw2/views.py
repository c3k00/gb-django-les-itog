from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Product, Order, OrderItem
from django.utils import timezone
from datetime import timedelta
from .forms import ClientForm, OrderForm, ProductForm
from django.db import transaction

def index(request):
    context = {
        "title": "Главная страница",
        "content": "Приветствую на главной странцие",
    }
    return render(request, 'index.html', context)

# Клиенты
def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'clients_list.html', {'clients': clients})

def client_detail(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, 'client_detail.html', {'client': client})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'edit_client.html', {'form': form})

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('clients_list')
    return render(request, 'delete_client.html', {'client': client})

# Продукты
def products_list(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})

def product_detail(request, id):
    products = get_object_or_404(Client, id=id)
    return render(request, 'products_detail.html', {'products': products})

def create_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        Product.objects.create(name=name, description=description, price=price)
        return redirect('products_list')
    return render(request, 'create_product.html')
#
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {'form': form})
#
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('products_list')
    return render(request, 'delete_product.html', {'product': product})

# Заказы
def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'orders_list.html', {'orders': orders})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.save()  # Сохраняем заказ, чтобы он получил первичный ключ
                # Сохраняем связанные объекты, если они есть
                form.save_m2m()  # Этот метод используется для сохранения полей ManyToMany

                # Если у вас есть OrderItem, создайте их здесь
                products = form.cleaned_data['products']
                for product in products:
                    OrderItem.objects.create(order=order, product=product, quantity=order.quantity)

            return redirect('orders_list')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    clients = Client.objects.all()
    products = Product.objects.all()
    order_products = [item.product.id for item in order.items.all()]
    if request.method == 'POST':
        order.client = get_object_or_404(Client, id=request.POST['client'])
        order.items.all().delete()
        for product_id in request.POST.getlist('products'):
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(order=order, product=product)
        order.save()
        return redirect('orders_list')
    return render(request, 'edit_order.html', {
        'order': order,
        'clients': clients,
        'products': products,
        'order_products': order_products,
    })

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('orders_list')
    return render(request, 'delete_order.html', {'order': order})

def ordered_products_view(request):
    # Получаем текущую дату и время
    now = timezone.now()

    # Фильтры по времени
    last_7_days = now - timedelta(days=7)
    last_30_days = now - timedelta(days=30)
    last_year = now - timedelta(days=365)

    # Заказы за разные периоды
    orders_last_7_days = Order.objects.filter(order_date__gte=last_7_days)
    orders_last_30_days = Order.objects.filter(order_date__gte=last_30_days)
    orders_last_year = Order.objects.filter(order_date__gte=last_year)

    # Уникальные товары за разные периоды
    products_last_7_days = {item.product for order in orders_last_7_days for item in order.order_items.all()}
    products_last_30_days = {item.product for order in orders_last_30_days for item in order.order_items.all()}
    products_last_year = {item.product for order in orders_last_year for item in order.order_items.all()}

    context = {
        'products_last_7_days': products_last_7_days,
        'products_last_30_days': products_last_30_days,
        'products_last_year': products_last_year,
    }

    return render(request, 'ordered_products.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    # order.total_amount = Order.save.self.total_amount
    return render(request, 'order_detail.html', {'order': order})

def order_success(request):
    return render(request, 'order_success.html')