from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from app_account.models import User
from app_account.serializers import UserRegisterSerializer
from django.core.exceptions import ValidationError
from django.urls import reverse

# Test for users models 
class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.assertEqual(user.phone, '09123456789')
        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(phone='09123456789', name='Admin User', password='admin123')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password('admin123'))

    def test_phone_validation(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(phone='123', name='Invalid Phone', password='password123')


# Test for serializers
class UserSerializerTest(TestCase):

    def test_register_serializer_valid(self):
        data = {
            'phone': '09123456789',
            'name': 'Test User',
            'password': 'password123'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_invalid_phone(self):
        data = {
            'phone': '123',
            'name': 'Test User',
            'password': 'password123'
        }
        serializer = UserRegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


# Test for views 
class UserViewTest(APITestCase):

    def test_register_user(self):
        data = {
            'phone': '09123456789',
            'name': 'Test User',
            'password': 'password123'
        }
        response = self.client.post(reverse('accounts:user_register'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'sms send.')

    def test_verify_user_code(self):
        #* Simulate OTP verification process (use mock in future if needed)
        pass

    def test_change_password(self):
        user = User.objects.create_user(phone='09123456789', name='Test User', password='password123')
        self.client.force_authenticate(user=user)
        data = {
            'old_password': 'password123',
            'new_password': 'newpassword123'
        }
        response = self.client.put(reverse('accounts:change_password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['password changed.'], 'password changed.')