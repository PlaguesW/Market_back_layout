from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_product.models import Product
from app_cart.cart import Cart
from app_account.models import User


# Tests for Cart class
class CartClassTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.request = self.client
        self.request.session = {}

    def test_add_to_cart(self):
        cart = Cart(self.request)
        cart.add(product_id=self.product.id, quantity=2)
        self.assertIn(str(self.product.id), cart.cart)
        self.assertEqual(cart.cart[str(self.product.id)]['quantity'], 2)

    def test_remove_from_cart(self):
        cart = Cart(self.request)
        cart.add(product_id=self.product.id, quantity=1)
        cart.remove(product_id=self.product.id)
        self.assertNotIn(str(self.product.id), cart.cart)

    def test_clear_cart(self):
        cart = Cart(self.request)
        cart.add(product_id=self.product.id, quantity=1)
        cart.clear()
        self.assertEqual(len(cart.cart), 0)

    def test_cart_total_price_with_discount(self):
        cart = Cart(self.request)
        cart.add(product_id=self.product.id, quantity=2)
        cart.detail(coupon=None)
        self.assertEqual(cart.cart['final_price'], 2000)  # 2 * 1000


# Тest for serializers
class CartViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.client.force_authenticate(user=self.user)

    def test_add_to_cart_view(self):
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(reverse('stroes:add_cart_item'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'product added.')

    def test_retrieve_cart_view(self):
        self.client.post(reverse('stroes:add_cart_item'), {'product_id': self.product.id, 'quantity': 2})
        response = self.client.get(reverse('stroes:cart_detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pay_price', response.data)

    def test_clear_cart_view(self):
        self.client.post(reverse('stroes:add_cart_item'), {'product_id': self.product.id, 'quantity': 1})
        response = self.client.delete(reverse('stroes:delete_cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'cart deleted.')

    def test_delete_cart_item_view(self):
        self.client.post(reverse('stroes:add_cart_item'), {'product_id': self.product.id, 'quantity': 1})
        response = self.client.delete(reverse('stroes:delete_cart_item', args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'product deleted.')