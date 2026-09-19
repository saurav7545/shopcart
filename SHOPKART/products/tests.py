from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product


class HomeTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class ProductTests(TestCase):
    def setUp(self):
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

    def test_search_view(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)

    def test_search_with_query(self):
        response = self.client.get(reverse("search") + "?q=Phone")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Phone")

    def test_product_detail(self):
        response = self.client.get(reverse("product_detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_category_view(self):
        response = self.client.get(reverse("category", args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_category_view_invalid_slug(self):
        response = self.client.get(reverse("category", args=["nonexistent"]))
        self.assertEqual(response.status_code, 404)
