from django.db import models
from ..models.productModel import Product
from django.contrib.auth.models import User

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    movement_type = models.CharField(max_length=7, choices=MOVEMENT_TYPES)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movement_type} - {self.quantity} de {self.product.name}"
