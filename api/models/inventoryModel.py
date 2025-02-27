from django.db import models
from ..models.productModel import Product

class Inventory(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),  # Disponible en stock
        ('used', 'Used'),  # Ya se usó (por receta o compra)
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse_location = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')  # Nuevo campo

    def __str__(self):
        return f"{self.product.name} - {self.quantity} ({self.status})"

