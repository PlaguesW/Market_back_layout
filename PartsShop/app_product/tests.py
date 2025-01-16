from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_account.models import User
from app_store.models import Store
from app_product.models import Product, Category


# Tests for Product and Category
class ProductModelTest(TestCase):

    def setUp(self):
        self.seller = User.objects.create_user(phone='09123456789', name='Seller User', password='password123', is_seller=True)
        self.store = Store.objects.create(
            founder=self.seller,
            name="Test Store",
            slug="test-store",
            description="This is a test store.",
            bank_number=1234567890123456,
        )
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_create_product(self):
        product = Product.objects.create(
            seller=self.store,
            category=self.category,
            name="Test Product",
            price=1000,
            stock=10,
            description="This is a test product.",
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.seller, self.store)
        self.assertEqual(product.category, self.category)
        self.assertTrue(product.is_exists)

    def test_product_stock(self):
        product = Product.objects.create(
            seller=self.store,
            category=self.category,
            name="Test Product",
            price=1000,
            stock=0,
            description="This is a test product.",
        )
        self.assertFalse(product.is_exists)

    def test_create_category(self):
        category = Category.objects.create(name="New Category", slug="new-category")
        self.assertEqual(category.name, "New Category")


# Tests for views
class ProductViewTest(APITestCase):

    def setUp(self):
        self.seller = User.objects.create_user(phone='09123456789', name='Seller User', password='password123', is_seller=True)
        self.store = Store.objects.create(
            founder=self.seller,
            name="Test Store",
            slug="test-store",
            description="This is a test store.",
            bank_number=1234567890123456,
        )
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.client.force_authenticate(user=self.seller)

    def test_create_product_view(self):
        data = {
            "category": self.category.id,
            "name": "Test Product",
            "price": 1000,
            "stock": 10,
            "description": "This is a test product.",
        }
        response = self.client.post(reverse('products:create_product'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'product created.')

    def test_update_product_view(self):
        product = Product.objects.create(
            seller=self.store,
            category=self.category,
            name="Old Product",
            price=500,
            stock=5,
            description="Old description.",
        )
        data = {
            "name": "Updated Product",
            "price": 1500,
        }
        response = self.client.put(reverse('products:update_product', args=[product.id]), data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        product.refresh_from_db()
        self.assertEqual(product.name, "Updated Product")
        self.assertEqual(product.price, 1500)

    def test_delete_product_view(self):
        product = Product.objects.create(
            seller=self.store,
            category=self.category,
            name="Test Product",
            price=1000,
            stock=10,
            description="This is a test product.",
        )
        response = self.client.delete(reverse('products:delete_product', args=[product.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'product deleted.')

    def test_get_product_list(self):
        Product.objects.create(seller=self.store, category=self.category, name="Product 1", price=1000, stock=10)
        Product.objects.create(seller=self.store, category=self.category, name="Product 2", price=2000, stock=5)
        response = self.client.get(reverse('products:show_list_products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_products_by_category(self):
        Product.objects.create(seller=self.store, category=self.category, name="Product 1", price=1000, stock=10)
        response = self.client.get(reverse('products:show_category_filter_product', args=[self.category.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
