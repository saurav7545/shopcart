from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Category, Product
from card.models import Cart, CartItem

User = get_user_model()


class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("cartuser", "cart@test.com", "password123")
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

    def test_cart_empty(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        response = self.client.get(reverse("add_to_cart", args=[self.product.id]))
        self.assertRedirects(response, reverse("cart"))
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)

    def test_add_to_cart_out_of_stock(self):
        self.product.stock = 0
        self.product.save()
        response = self.client.get(reverse("add_to_cart", args=[self.product.id]))
        self.assertRedirects(response, reverse("product_detail", args=[self.product.id]))

    def test_remove_one_from_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.get(reverse("remove_one_from_cart", args=[self.product.id]))
        self.assertRedirects(response, reverse("cart"))
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_cart_item(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.get(reverse("remove_cart_item", args=[self.product.id]))
        self.assertRedirects(response, reverse("cart"))
        self.assertEqual(CartItem.objects.filter(cart=cart, product=self.product).count(), 0)
