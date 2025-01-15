from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_account.models import User
from app_product.models import Product
from app_like.models import Like
from app_like.serialisers import LikeSerializer


# Tests for likes
class LikeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)

    def test_create_like(self):
        like = Like.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.product, self.product)

    def test_unique_like(self):
        Like.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:30:00')


# Tests for likres serializers
class LikeSerializerTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.valid_data = {'product_id': self.product.id}
        self.invalid_data = {'product_id': 999}  # Non-existet product

    def test_like_serializer_valid(self):
        serializer = LikeSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_like_serializer_invalid(self):
        serializer = LikeSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)


# Test for views
class LikeViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.client.force_authenticate(user=self.user)

    def test_like_product(self):
        data = {'product_id': self.product.id}
        response = self.client.post(reverse('likes:like_product'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'liked success')

    def test_like_duplicate_product(self):
        Like.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        data = {'product_id': self.product.id}
        response = self.client.post(reverse('likes:like_product'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'this product already liked by you')

    def test_dislike_product(self):
        Like.objects.create(user=self.user, product=self.product, register_date='2025-01-01 12:00:00')
        data = {'product_id': self.product.id}
        response = self.client.post(reverse('likes:dislike_product'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'like for this produc deleted success')

    def test_dislike_non_liked_product(self):
        data = {'product_id': self.product.id}
        response = self.client.post(reverse('likes:dislike_product'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'you not like this product')