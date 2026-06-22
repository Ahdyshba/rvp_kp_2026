from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import Product, Category

User = get_user_model()

# проверка моделей
class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Гитары")
        self.product = Product.objects.create(
            name="Ibanez RGA7",
            price=70000,
            stock=5,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Ibanez RGA7")
        self.assertEqual(self.product.price, 70000)
        self.assertEqual(self.product.stock, 5)
        self.assertEqual(self.product.category.name, "Гитары")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Ibanez RGA7")


# проверка API
class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', password='rimpmpss90')
        self.category = Category.objects.create(name="Гитары")
        self.product = Product.objects.create(
            name="Jackson Stars Soloist SL7-J2B",
            price=150000,
            stock=2,
            category=self.category
        )

    def test_get_products_unauthorized(self):
        """Неавторизованный запрос, должен вернуть 401"""
        response = self.client.get('/api/catalog/products/')
        self.assertEqual(response.status_code, 401)

    def test_get_products_authorized(self):
        """Авторизованный запрос, должен вернуть 200"""
        access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/catalog/products/')
        self.assertEqual(response.status_code, 200)

    def test_create_product_authorized(self):
        """Авторизованный POST, должен создать товар"""
        access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post('/api/catalog/products/', {
            'name': 'SCHECTER PT SPECIAL',
            'description': 'Отличная электрогитара',
            'price': 80000,
            'stock': 3,
            'is_active': True, 
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)