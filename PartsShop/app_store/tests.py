from django.test import TestCase

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app_account.models import User
from app_store.models import Store, StoreCheckout
from datetime import datetime


# Tests Store and StoreCheckout
class StoreModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123', is_seller=True)
        self.store = Store.objects.create(
            founder=self.user,
            name="Test Store",
            slug="test-store",
            description="This is a test store.",
            wallet=50000,
            bank_number=1234567890123456,
        )

    def test_create_store(self):
        self.assertEqual(self.store.founder, self.user)
        self.assertEqual(self.store.name, "Test Store")
        self.assertEqual(self.store.wallet, 50000)

    def test_store_checkout(self):
        checkout = StoreCheckout.objects.create(
            store=self.store,
            amount=10000,
            pay_date=datetime.now(),
        )
        self.assertEqual(checkout.store, self.store)
        self.assertEqual(checkout.amount, 10000)
        self.assertEqual(self.store.wallet, 40000) 


# Tests for views
class StoreViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone='09123456789', name='Test User', password='password123', is_seller=True)
        self.client.force_authenticate(user=self.user)

    def test_create_store_view(self):
        data = {
            "name": "New Store",
            "slug": "new-store",
            "description": "This is a new store.",
            "bank_number": 1234567890123456,
        }
        response = self.client.post(reverse('stores:create_store'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'store created')
        store = Store.objects.filter(founder=self.user).first()
        self.assertIsNotNone(store)

    def test_update_store_view(self):
        store = Store.objects.create(
            founder=self.user,
            name="Test Store",
            slug="test-store",
            description="Old description.",
            bank_number=1234567890123456,
        )
        data = {
            "description": "Updated description.",
        }
        response = self.client.put(reverse('stores:update_store'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        store.refresh_from_db()
        self.assertEqual(store.description, "Updated description.")

    def test_retrieve_store_view(self):
        store = Store.objects.create(
            founder=self.user,
            name="Test Store",
            slug="test-store",
            description="This is a test store.",
            bank_number=1234567890123456,
        )
        response = self.client.get(reverse('stores:retrieve_store'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], store.name)

    def test_store_checkout_view(self):
        store = Store.objects.create(
            founder=self.user,
            name="Test Store",
            slug="test-store",
            wallet=50000,
            bank_number=1234567890123456,
        )
        data = {
            "amount": 10000,
            "bank_number": 1234567890123456,
        }
        response = self.client.post(reverse('stores:checkout_store'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'checkout success.')
        store.refresh_from_db()
        self.assertEqual(store.wallet, 40000)

    def test_retrieve_store_checkouts(self):
        store = Store.objects.create(
            founder=self.user,
            name="Test Store",
            slug="test-store",
            wallet=50000,
            bank_number=1234567890123456,
        )
        StoreCheckout.objects.create(store=store, amount=10000, pay_date=datetime.now())
        response = self.client.get(reverse('stores:checkout_store'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)