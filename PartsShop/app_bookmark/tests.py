from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_bookmark.models import Bookmark
from app_product.models import Product
from app_account.models import User
from app_bookmark.serializers import CreateBookmarkSerializer, ListBookmarkSerializer

# Tests for bookmark models
class BookmarkModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
    
    def test_create_bookmark(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.product, self.product)

    def test_unique_bookmark(self):
        Bookmark.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        with self.assertRaises(Exception):
            Bookmark.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')


# Tests for serializers
class BookmarkSerializerTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.valid_data = {'product_id': self.product.id}
        self.invalid_data = {'product_id': 999}

    def test_create_bookmark_serializer_valid(self):
        serializer = CreateBookmarkSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_create_bookmark_serializer_invalid(self):
        serializer = CreateBookmarkSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)


# Test for views  
class BookmarkViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.client.force_authenticate(user=self.user)

    def test_add_bookmark(self):
        data = {'product_id': self.product.id}
        response = self.client.post(reverse('bookmarks:add_bookmark'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'product added to your bookmarks')

    def test_add_duplicate_bookmark(self):
        Bookmark.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        data = {'product_id': self.product.id}
        response = self.client.post(reverse('bookmarks:add_bookmark'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'this product already added to your bookmarks')

    def test_list_bookmarks(self):
        Bookmark.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        response = self.client.get(reverse('bookmarks:show_bookmark'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_bookmark(self):
        bookmark = Bookmark.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        response = self.client.delete(reverse('bookmarks:delete_bookmark', args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'product deleted of bookmarks')