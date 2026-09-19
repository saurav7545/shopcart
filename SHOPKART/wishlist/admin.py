from django.contrib import admin

from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "product",
        "created_at",
    )

    list_filter = (
        "product",
        "user",
    )

    search_fields = (
        "user__username",
        "product__name",
    )
