from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from products.models import Product

from .models import Wishlist as WishlistModel


@login_required
def wishlist_view(request):

    items = WishlistModel.objects.filter(
        user=request.user
    ).select_related(
        "product"
    )

    return render(
        request,
        "wishlist.html",
        {
            "items": items
        }
    )


@login_required
def add_wishlist(
    request,
    product_id
):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    _, created = WishlistModel.objects.get_or_create(

        user=request.user,

        product=product
    )

    if created:

        messages.success(
            request,
            "Added to wishlist."
        )

    else:

        messages.info(
            request,
            "Already in wishlist."
        )

    return redirect(
        "product_detail",
        product_id=product.id
    )


@login_required
def remove_wishlist(
    request,
    product_id
):

    WishlistModel.objects.filter(

        user=request.user,

        product_id=product_id

    ).delete()

    messages.success(
        request,
        "Removed from wishlist."
    )

    return redirect(
        "wishlist"
    )
