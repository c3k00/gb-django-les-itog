"""
URL configuration for hw2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path#, include

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    # Клиенты
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/<int:id>/', views.client_detail, name='client_detail'),
    path('clients/create/', views.create_client, name='create_client'),
    path('clients/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('clients/delete/<int:client_id>/', views.delete_client, name='delete_client'),

    # Продукты
    path('products/', views.products_list, name='products_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    #
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/', views.product_list, name='product_list'),
    # Заказы
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('ordered-products/', views.ordered_products_view, name='ordered_products'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),  # Добавьте этот путь
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)