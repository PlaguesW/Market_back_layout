from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_account.models import User
from app_product.models import Product
from app_comment.models import Comment
from app_comment.serializers import CommentSerializer


# Tests for comment
class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)

    def test_create_comment(self):
        comment = Comment.objects.create(
            writer=self.user,
            product=self.product,
            body="This is a test comment.",
            register_date='2025-01-01 12:00:00',
            is_confirm=True,
        )
        self.assertEqual(comment.writer, self.user)
        self.assertEqual(comment.product, self.product)
        self.assertTrue(comment.is_confirm)
        self.assertEqual(comment.body, "This is a test comment.")

    def test_create_sub_comment(self):
        parent_comment = Comment.objects.create(
            writer=self.user,
            product=self.product,
            body="Parent comment.",
            register_date='2025-01-01 12:00:00',
            is_confirm=True,
        )
        sub_comment = Comment.objects.create(
            writer=self.user,
            product=self.product,
            body="This is a sub comment.",
            sub_comment=parent_comment,
            register_date='2025-01-01 12:30:00',
            is_confirm=True,
        )
        self.assertEqual(sub_comment.sub_comment, parent_comment)


# Test for serializers
class CommentSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.valid_data = {
            "writer": self.user.id,
            "product": self.product.id,
            "body": "This is a valid comment.",
        }
        self.invalid_data = {
            "writer": self.user.id,
            "product": 999,  # Non-existent product
            "body": "This is an invalid comment.",
        }

    def test_comment_serializer_valid(self):
        serializer = CommentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_comment_serializer_invalid_product(self):
        serializer = CommentSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('product', serializer.errors)


# Test for views 
class CommentViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.client.force_authenticate(user=self.user)

    def test_create_comment_view(self):
        data = {
            "product": self.product.id,
            "body": "This is a test comment.",
        }
        response = self.client.post(reverse('comments:create_comment'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'comment created success')

    def test_list_comments_view(self):
        Comment.objects.create(writer=self.user, product=self.product, body="Test Comment", is_confirm=True)
        response = self.client.get(reverse('comments:list_of_comment'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)