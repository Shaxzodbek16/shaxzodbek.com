from django.contrib.auth.hashers import check_password
from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='password123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertTrue(self.user.check_password('password123'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertIsNotNone(self.user.date_joined)

    def test_slug_generation(self):
        self.assertEqual(self.user.slug, 'test-user')
        self.user.name = 'Test User Updated'
        self.user.save()
        self.assertEqual(self.user.slug, 'test-user')

    def test_string_representation(self):
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_user(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(check_password('password123', self.user.password), True)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.slug, 'test-user')
        self.assertEqual(self.user.__str__(), self.user.email)
