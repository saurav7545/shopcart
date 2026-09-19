from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(
        max_length=200
    )

    title = models.CharField(
        max_length=300
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    image = models.URLField(
        blank=True
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    discount = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class ProductReview(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "product",
            "user"
        )

    def __str__(self):

        return (
            f"{self.product.name} - "
            f"{self.user.username}"
        )