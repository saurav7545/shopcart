from django.urls import path
from . import views


urlpatterns = [

    # Cart page
    path(
        "",
        views.cart,
        name="cart"
    ),

    # Add / increase quantity
    path(
        "add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # Decrease quantity
    path(
        "remove-one/<int:product_id>/",
        views.remove_one_from_cart,
        name="remove_one_from_cart"
    ),

    # Remove complete item
    path(
        "remove/<int:product_id>/",
        views.remove_cart_item,
        name="remove_cart_item"
    ),

    # Save for later (move to wishlist)
    path(
        "save/<int:product_id>/",
        views.save_for_later,
        name="save_for_later"
    ),

]