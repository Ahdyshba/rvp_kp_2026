from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser1',
            email='test1@pochta.ru',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser1')
        self.assertEqual(user.email, 'test1@pochta.ru')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin2',
            email='admin2@pochta.ru',
            password='adminpass123'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)