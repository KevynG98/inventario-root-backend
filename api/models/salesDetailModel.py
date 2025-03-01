from django.db import models
from .salesModel import Sale
from .productModel import Product

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        managed = False  # Django no creará ni modificará la tabla en la BD
        db_table = "category" 

    def __str__(self):
        return f"Detalle de Venta #{self.sale.id} - {self.product.name}"
