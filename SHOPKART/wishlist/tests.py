from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Category, Product
from wishlist.models import Wishlist

User = get_user_model()


class WishlistTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("wishuser", "wish@test.com", "password123")
        self.category = Category.objects.create(name="Mobile", slug="mobile")
        self.product = Product.objects.create(
            name="Test Phone",
            title="Test Phone Title",
            description="Test description",
            price=999.99,
            category=self.category,
            stock=10,
            brand="TestBrand",
        )
        self.client.force_login(self.user)

    def test_wishlist_view(self):
        response = self.client.get(reverse("wishlist"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_wishlist(self):
        response = self.client.get(reverse("add_wishlist", args=[self.product.id]))
        self.assertRedirects(response, reverse("product_detail", args=[self.product.id]))
        self.assertEqual(Wishlist.objects.filter(user=self.user, product=self.product).count(), 1)

    def test_add_duplicate_wishlist(self):
        Wishlist.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse("add_wishlist", args=[self.product.id]))
        self.assertRedirects(response, reverse("product_detail", args=[self.product.id]))
        self.assertEqual(Wishlist.objects.filter(user=self.user, product=self.product).count(), 1)

    def test_remove_from_wishlist(self):
        Wishlist.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse("remove_wishlist", args=[self.product.id]))
        self.assertRedirects(response, reverse("wishlist"))
        self.assertEqual(Wishlist.objects.filter(user=self.user, product=self.product).count(), 0)
