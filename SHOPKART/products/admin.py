from django.contrib import admin

from .models import (
    Product,
    Category,
    ProductReview
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name"
    )

    search_fields = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "price",
        "stock",
        "brand",
        "rating",
        "is_active"
    )

    list_filter = (
        "is_active",
        "category",
        "brand"
    )

    search_fields = (
        "name",
        "title",
        "brand"
    )


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "user",
        "rating",
        "created_at"
    )

    list_filter = (
        "rating",
    )