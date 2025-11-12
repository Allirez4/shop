from django.db import models
from decimal import Decimal
from accounts.models import CustomUser
from home.models import Product

class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='order')
    created_at=models.DateTimeField(auto_now_add=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=20)
    #totalprice=models.DecimalField(max_digits=6,decimal_places=2)
    extrainfo=models.TextField(null=True,blank=True)
    #items_order=models.ForeignKey(OrderItems,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)
    delivery_date=models.DateTimeField()
    delivery_fee=models.DecimalField(max_digits=3,decimal_places=2)
    authority=models.CharField(max_length=70)
    is_deliverd=models.BooleanField(default=False)
    def get_order_total(self):
        subtotal=sum(item.price_at * item.quantity for item in self.items.all())
        tax=subtotal*Decimal(0.10)
        total=subtotal+tax+Decimal(self.delivery_fee)
        return total
    class Meta:
        ordering=('created_at',)
        verbose_name=('order',)
        verbose_name_plural='orders'
    def __str__(self):
        return str(self.id)    
class OrderItems(models.Model):
        item=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pname')
        price_at=models.DecimalField(max_digits=6,decimal_places=2)
        quantity=models.SmallIntegerField()
        order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')