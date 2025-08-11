import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Product, Order, OrderItem
from django.db.models import Q
from decimal import Decimal, InvalidOperation


def index(request):
    return render(request, 'platform/index.html')


def logout_view(request):
    logout(request)
    return redirect('platform:index')


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "platform/product.html", {"products": products})


@login_required
def home(request):
    return render(request, 'platform/home.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, "User already exists.")
            return redirect("platform:signup")
        else:
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, "Signup successful. Please log in.")
            return redirect("platform:login_user")
    return render(request, 'platform/signup.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("platform:home")
        messages.error(request, "Invalid credentials.")
        return redirect("platform:login_user")
    return render(request, 'platform/login.html')


def my_account(request):
    orders = request.user.order_set.filter(is_paid=True).order_by('-created_at')

    if request.method == "POST" and request.POST.get("form_name") == "password_change":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password updated successfully.")
            return redirect("platform:my_account")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "platform/my_account.html", {
        "user": request.user,
        "orders": orders,
        "password_form": form,
    })


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    try:
        quantity = Decimal(request.POST.get('quantity', '0'))
        if quantity <= 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        messages.warning(request, "Invalid quantity entered.")
        return redirect('platform:product_list')

    product = get_object_or_404(Product, id=product_id)

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + float(quantity)

    request.session['cart'] = cart
    messages.success(request, f"Added {quantity}kg of {product.product_name} to cart.")
    return redirect('platform:product_list')


@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items, total_price = get_cart_details(cart)

    return render(request, 'platform/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def remove_item(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] -= 1
        if cart[product_id_str] <= 0:
            del cart[product_id_str]
        request.session['cart'] = cart

    return redirect("platform:view_cart")


@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    # Check stock
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = Decimal(str(quantity))
        if quantity > product.product_stock:
            messages.error(request, f"Not enough stock for {product.product_name}")
            return redirect("platform:view_cart")

    # Generate invoice_id and create order
    invoice_id = uuid.uuid4()
    order = Order.objects.create(user=request.user, invoice_id=invoice_id)

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = Decimal(str(quantity))
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.product_price)

    request.session['invoice_id'] = str(invoice_id)
    return redirect('payments:checkout_summary')


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    total = sum(item.subtotal for item in items)

    return render(request, 'platform/order_confirmation.html', {
        'order': order,
        'items': items,
        'total': total,
    })


def order_history(request):
    orders = Order.objects.filter(user=request.user, is_paid=True).order_by('-created_at')

    # Attach items directly instead of recalculating subtotals
    for order in orders:
        order.items_with_subtotals = order.items.all()

    return render(request, 'platform/order_history.html', {"orders": orders})


# ✅ Reusable helper
def get_cart_details(cart):
    items = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        quantity_decimal = Decimal(str(quantity))
        subtotal = quantity_decimal * product.product_price
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity_decimal,
            'subtotal': subtotal,
            'total_price': subtotal  # ✅ Add this lin
        })
    return items, total


def admin_dashboard(request):
    paid_orders = Order.objects.filter(is_paid=True).exclude(total_price=0)

    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', '-created_at')

    if query:
        paid_orders = paid_orders.filter(
            Q(user__username__icontains=query) |
            Q(invoice_id__icontains=query)
        )

    paid_orders = paid_orders.order_by(sort_by)

    return render(request, 'platform/admin_dashboard.html', {
        "orders": paid_orders,
        "query": query,
        "sort_by": sort_by
    })


@staff_member_required
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "platform/order_detail_admin.html", {"order": order})
