from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Category, Product
from card.models import Cart, CartItem
from orders.models import Order, OrderItem, Coupon

User = get_user_model()


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("orderuser", "order@test.com", "password123")
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

    def test_checkout_empty_cart(self):
        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("cart"))

    def test_checkout_success(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        initial_stock = self.product.stock
        response = self.client.post(reverse("checkout"), {
            "full_name": "Test User",
            "phone": "1234567890",
            "address": "123 Test St",
            "city": "TestCity",
            "state": "TestState",
            "pincode": "123456",
        })
        self.assertRedirects(response, reverse("order_success", args=[Order.objects.first().id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 1)

    def test_order_creation(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.post(reverse("checkout"), {
            "full_name": "Test User",
            "phone": "1234567890",
            "address": "123 Test St",
            "city": "TestCity",
            "state": "TestState",
            "pincode": "123456",
        })
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(str(order.total_amount), "1999.98")
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(str(order.items.first().price), "999.99")

    def test_cancel_order_restores_stock(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Test User",
            phone="1234567890",
            address="123 Test St",
            city="TestCity",
            state="TestState",
            pincode="123456",
            total_amount=999.99,
        )
        initial_stock = self.product.stock
        response = self.client.get(reverse("cancel_order", args=[order.id]))
        self.assertRedirects(response, reverse("order_detail", args=[order.id]))
        order.refresh_from_db()
        self.assertEqual(order.status, "cancelled")
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock)

    def test_my_orders(self):
        Order.objects.create(
            user=self.user,
            full_name="Test User",
            phone="1234567890",
            address="123 Test St",
            city="TestCity",
            state="TestState",
            pincode="123456",
            total_amount=999.99,
        )
        response = self.client.get(reverse("my_orders"))
        self.assertEqual(response.status_code, 200)

    def test_order_detail(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Test User",
            phone="1234567890",
            address="123 Test St",
            city="TestCity",
            state="TestState",
            pincode="123456",
            total_amount=999.99,
        )
        response = self.client.get(reverse("order_detail", args=[order.id]))
        self.assertEqual(response.status_code, 200)


class CouponTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("coupuser", "coup@test.com", "password123")
        self.category = Category.objects.create(name="Mobile", slug="mobile")
        self.product = Product.objects.create(
            name="Test Phone",
            title="Test Phone Title",
            description="Test description",
            price=1000.00,
            category=self.category,
            stock=10,
            brand="TestBrand",
        )
        self.client.force_login(self.user)

    def test_coupon_valid(self):
        Coupon.objects.create(code="SAVE10", discount_percent=10, active=True, minimum_amount=0)
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(reverse("checkout"), {
            "full_name": "Test User",
            "phone": "1234567890",
            "address": "123 Test St",
            "city": "TestCity",
            "state": "TestState",
            "pincode": "123456",
            "coupon_code": "SAVE10",
        })
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(str(order.total_amount), "900.00")

    def test_coupon_invalid(self):
        Coupon.objects.create(code="SAVE10", discount_percent=10, active=True, minimum_amount=0)
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        response = self.client.post(reverse("checkout"), {
            "full_name": "Test User",
            "phone": "1234567890",
            "address": "123 Test St",
            "city": "TestCity",
            "state": "TestState",
            "pincode": "123456",
            "coupon_code": "INVALID",
        })
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, 1000.00)
