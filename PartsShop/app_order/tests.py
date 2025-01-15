from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_account.models import User
from app_product.models import Product
from app_order.models import Order, OrderItem, Coupon
from datetime import datetime, timedelta


# Tests for Order, OrderItem и Coupon
class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.order = Order.objects.create(owner=self.user, total_price=1000, pay_price=900, discount=100, pay_date=datetime.now())

    def test_create_order(self):
        self.assertEqual(self.order.owner, self.user)
        self.assertEqual(self.order.total_price, 1000)
        self.assertEqual(self.order.pay_price, 900)
        self.assertEqual(self.order.discount, 100)

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, price=1000, quantity=2)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.total_price(), 2000)

    def test_create_coupon(self):
        coupon = Coupon.objects.create(code="TEST10", valid_from=datetime.now(), valid_to=datetime.now() + timedelta(days=1), discount=10)
        self.assertEqual(coupon.code, "TEST10")
        self.assertTrue(Coupon.active.filter(code="TEST10").exists())


# Tests for views
class OrderViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.product = Product.objects.create(name='Test Product', price=1000, stock=10, is_confirm=True)
        self.client.force_authenticate(user=self.user)

    def test_checkout_without_coupon(self):
        # Add product into cart
        self.client.post(reverse('stroes:add_cart_item'), {'product_id': self.product.id, 'quantity': 1})

        # Make order
        response = self.client.get(reverse('orders:checkout_cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'your cart is paid success.')

        # Check that the order has been created
        order = Order.objects.filter(owner=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 1000)

    def test_checkout_with_coupon(self):
        # Make a coupon
        Coupon.objects.create(code="DISCOUNT10", valid_from=datetime.now(), valid_to=datetime.now() + timedelta(days=1), discount=10)

        # Add product into cart
        self.client.post(reverse('stroes:add_cart_item'), {'product_id': self.product.id, 'quantity': 1})

        # Make order with active coupon
        response = self.client.get(reverse('orders:checkout_cart_with_coupon', args=["DISCOUNT10"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'your cart is paid success.')

        # Check the discount is apply
        order = Order.objects.filter(owner=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.pay_price, 900)  # discount 10% from 1000

    def test_checkout_empty_cart(self):
        response = self.client.get(reverse('orders:checkout_cart'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'your cart is empy')