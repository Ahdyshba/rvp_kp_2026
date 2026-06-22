from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import Cart, CartItem
from catalog.models import Product, Category

User = get_user_model()

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', password='rimpmpass90')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user.username, "useruser")

class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', password='rimpmpass90')
        self.category = Category.objects.create(name="Гитары")
        self.product = Product.objects.create(
            name="Ibanez RGA7",
            price=70000,
            stock=5,
            category=self.category
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

    def test_get_cart_unauthorized(self):
        response = self.client.get('/api/cart/carts/')
        self.assertEqual(response.status_code, 401)

    def test_get_cart_authorized(self):
        access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/cart/carts/')
        self.assertEqual(response.status_code, 200)