from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, Order, Wishlist
from django.contrib.auth.models import User 
from .models import Notification

def home(request):
    return render(request, 'home.html')

def aboutus_view(request):
    return render(request, 'aboutus.html')

def contactus_view(request):
    return render(request, 'contactus.html')

def product_list(request):
    query = request.GET.get('q') 
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user) 
    else:
        wishlist_items = []
    context = {
        'products': products,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'product_list.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'  
    success_url = reverse_lazy('')  

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print("Attempting to reset password for user:", username)
            try:
                user = User.objects.get(username=username)
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                print("Password updated successfully.")  
                return redirect('login') 
            except User.DoesNotExist:
                form.add_error(None, "User does not exist.")
    else:
        form = PasswordResetForm()
    return render(request, 'password_rest.html', {'form': form})

@login_required
def my_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    products_in_cart = cart.products.all() if cart.products.exists() else None
    return render(request, 'my_cart.html', {'products': products_in_cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect('my_cart')

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product_to_remove = get_object_or_404(Product, id=product_id)
    cart.products.remove(product_to_remove)
    return redirect('my_cart')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    
    if request.method == 'POST':
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user, 
            address=address, 
            contact_number=contact_number, 
            payment_method=payment_method
        )

        order.products.set(cart.products.all())

        order.save()

        order.estimated_delivery_date = order.calculate_estimated_delivery_date()
        
        order.save()

        admin_users = User.objects.filter(is_staff=True)
        for admin in admin_users:
            Notification.objects.create(
                admin_user=admin,
                message=f"New order placed by {request.user.username}. Order ID: {order.id}"
            )

        if payment_method == "COD":
            order.payment_method = "COD"
            order.is_paid = False
            order.save()  
            cart.products.clear()
            return render(request, 'cod_success.html', {'order': order})

        elif payment_method == "UPI":
            order.payment_method = "UPI"
            order.is_paid = False
            order.save()  
            cart.products.clear()
            return render(request, 'upi_payment.html', {'order': order})

    return render(request, 'checkout.html', {'cart': cart})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.days_until_delivery() > 3 and not order.is_canceled:
        order.is_canceled = True
        order.save()
        messages.success(request, "Your order has been canceled successfully.")
    else:
        messages.error(request, "You cannot cancel this order as it is less than 3 days until delivery.")
    return redirect('my_orders')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product') if request.user.is_authenticated else []
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, wishlist_item_id):
    print(f"Attempting to remove wishlist item with ID: {wishlist_item_id} for user: {request.user.id}")
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, "Item removed from your wishlist.")
    return redirect('wishlist')

def remove_from_wishlist(request, wishlist_item_id):
    try:
        wishlist_item = Wishlist.objects.get(id=wishlist_item_id, user=request.user)
        wishlist_item.delete()
        return redirect('wishlist')
    except Wishlist.DoesNotExist:
        return redirect('wishlist') 

       
        

    



    
  
    

