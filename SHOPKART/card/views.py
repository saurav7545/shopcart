from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .models import Cart, CartItem
from wishlist.models import Wishlist


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    if product.stock <= 0:

        messages.error(
            request,
            "Product is out of stock."
        )

        return redirect(
            "product_detail",
            product_id=product.id
        )

    cart, _ = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:

        item.quantity = 1

    else:

        if item.quantity >= product.stock:

            messages.warning(
                request,
                "Maximum available stock already added."
            )

            return redirect("cart")

        item.quantity += 1

    item.save()

    return redirect("cart")

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related("product")

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(
    request,
    "cart.html",
    {
        "cart": cart,
        "items": items,
        "total": total,
    }
)

@login_required
def remove_one_from_cart(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

    else:

        cart_item.delete()

    return redirect("cart")

@login_required
def remove_cart_item(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id
    )

    cart_item.delete()

    return redirect("cart")

@login_required
def save_for_later(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_item = get_object_or_404(
        CartItem,
        cart=cart,
        product_id=product_id
    )

    cart_item.delete()

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(
        request,
        f"{product.name} saved for later."
    )

    return redirect("cart")
