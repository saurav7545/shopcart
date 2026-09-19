from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("Home.urls")
    ),

    path(
        "products/",
        include("products.urls")
    ),

    path(
        "card/",
        include("card.urls")
    ),

    path(
        "user/",
        include("user.urls")
    ),

    path(
        "orders/",
        include("orders.urls")
    ),

    path(
        "wishlist/",
        include("wishlist.urls")
    ),
]

handler404 = 'Home.views.page_not_found'
handler500 = 'Home.views.server_error'