from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from card.models import Cart, CartItem
from products.models import Product
from .models import (
    Order,
    OrderItem,
    ReturnRequest,
    Coupon
)


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    if product.stock <= 0:
        messages.error(request, "Product is out of stock.")
        return redirect("product_detail", product_id=product.id)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("checkout")


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related(
        "product"
    )

    if not items.exists():
        messages.warning(
            request,
            "Your cart is empty."
        )
        return redirect("cart")

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    coupon = None
    discount_amount = 0
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code", "").strip()

        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    code=coupon_code,
                    active=True,
                )
                if coupon.expiry_date and coupon.expiry_date <= timezone.now():
                    messages.error(
                        request,
                        "This coupon has expired."
                    )
                    coupon = None
                elif total < coupon.minimum_amount:
                    messages.error(
                        request,
                        f"Minimum order amount of ₹{coupon.minimum_amount} required."
                    )
                    coupon = None
                else:
                    discount_amount = total * Decimal(coupon.discount_percent) / Decimal(100)
                    total -= discount_amount
                    total = total.quantize(Decimal("0.01"))

            except Coupon.DoesNotExist:
                messages.error(
                    request,
                    "Invalid coupon code."
                )
                coupon = None

        if not coupon:
            total = sum(
                item.product.price * item.quantity
                for item in items
            )

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method", "cod")

        if payment_method not in dict(Order.PAYMENT_CHOICES):
            payment_method = "cod"

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                total_amount=total,
                payment_method=payment_method,
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            for item in items:
                item.product.stock -= item.quantity
                item.product.save(
                    update_fields=["stock"]
                )

            cart.items.all().delete()

        messages.success(
            request,
            f"Order #{order.id} placed successfully!"
        )

        return redirect(
            "order_success",
            order_id=order.id
        )

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(
        request,
        "checkout.html",
        {
            "cart": cart,
            "items": items,
            "total": total,
            "coupon": coupon,
        }
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "order_success.html",
        {
            "order": order
        }
    )


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders
        }
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "order_detail.html",
        {
            "order": order
        }
    )


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status not in [
        "pending",
        "confirmed"
    ]:
        messages.error(
            request,
            "This order cannot be cancelled."
        )

        return redirect(
            "order_detail",
            order_id=order.id
        )

    order.status = "cancelled"

    order.save(
        update_fields=["status"]
    )

    for item in order.items.select_related(
        "product"
    ):
        item.product.stock += item.quantity

        item.product.save(
            update_fields=["stock"]
        )

    messages.success(
        request,
        "Order cancelled successfully."
    )

    return redirect(
        "order_detail",
        order_id=order.id
    )


@login_required
def request_return(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status != "delivered":
        messages.error(
            request,
            "Only delivered orders can be returned."
        )

        return redirect(
            "order_detail",
            order_id=order.id
        )

    if hasattr(order, "return_request"):
        messages.info(
            request,
            "Return request already exists."
        )

        return redirect(
            "order_detail",
            order_id=order.id
        )

    if request.method == "POST":
        reason = request.POST.get(
            "reason",
            ""
        ).strip()

        if not reason:
            messages.error(
                request,
                "Please provide a reason."
            )

            return redirect(
                "order_detail",
                order_id=order.id
            )

        ReturnRequest.objects.create(
            order=order,
            reason=reason
        )

        messages.success(
            request,
            "Return request submitted."
        )

        return redirect(
            "order_detail",
            order_id=order.id
        )

    return render(
        request,
        "return.html",
        {
            "order": order
        }
    )