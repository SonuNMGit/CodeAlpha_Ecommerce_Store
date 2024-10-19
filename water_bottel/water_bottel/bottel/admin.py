from django.contrib import admin
from .models import Product
from .models import Order
from .models import Notification

admin.site.register(Product)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'contact_number', 'payment_method', 'is_paid', 'is_canceled', 'created_at','delivery_status')
    list_editable = ('is_paid','is_canceled','delivery_status',)
    list_filter = ('payment_method', 'is_paid', 'is_canceled','delivery_status') 
    search_fields = ('user__username', 'contact_number', 'payment_method')
    readonly_fields = ('created_at',)  
 
    def delivery_status_display(self, obj):
        return "delivered" if obj.is_paid else "Not delivered"
    delivery_status_display.short_description = 'delivery Status'

    def is_paid_display(self, obj):
        return "Paid" if obj.is_paid else "Not Paid"
    is_paid_display.short_description = 'Payment Status'

    def products_display(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    
    products_display.short_description = 'Products'

admin.site.register(Order, OrderAdmin)

class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['notifications'] = Notification.objects.filter(is_read=False)
        return context

admin_site = CustomAdminSite(name='custom_admin')

admin_site.register(Order)
admin_site.register(Notification)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
    list_editable = ('is_read',)
admin.site.register(Notification, NotificationAdmin)

