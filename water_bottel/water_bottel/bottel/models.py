from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from datetime import timedelta

class Product(models.Model):
    name = models.CharField(max_length=255)  
    description = models.TextField()         
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    image = models.ImageField(upload_to='products/') 
    eco_friendly = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.name
        
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    products = models.ManyToManyField(Product, blank=True) 

    def __str__(self):
        return f"Cart of {self.user.username}"

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD_CHOICES, default='COD')
    is_paid = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def days_until_delivery(self):
        estimated_date = self.calculate_estimated_delivery_date()
        return (estimated_date - timezone.now()).days
    
    def calculate_estimated_delivery_date(self):
        if self.created_at is None:
            return None  
        return self.created_at + timedelta(days=7)

    def save(self, *args, **kwargs):
        if not self.estimated_delivery_date:
            self.estimated_delivery_date = self.calculate_estimated_delivery_date()
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"
    
class Notification(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.admin_user.username} - {self.message}"


