from django.db import models
from django.utils import timezone

class Client(models.Model):
    """Модель клиента"""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)
    registration_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    quantity = models.IntegerField(default=0)
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )

    def __str__(self):
        return f'Order {self.id} by {self.client.name}'
    
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)  # Сначала сохраняем сам объект
        self.total_amount = sum(item.product.price * item.quantity for item in self.order_items.all())
        super(Order, self).save(*args, **kwargs)  # Снова сохраняем, чтобы сохранить вычисленное значение
        
    def __str__(self):
        return f"Order {self.id} by {self.client.name}"

class OrderItem(models.Model):
    """Связующая модель для заказов и товаров"""
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
