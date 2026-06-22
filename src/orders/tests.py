from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import Order, OrderItem
from catalog.models import Product, Category

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', password='rimpmpass90')
        self.order = Order.objects.create(
            user=self.user,
            total_price=150000,
            delivery_address="ул. Пушкина, д. 10",
            phone="+7 999 123-45-67"
        )

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, "useruser")
        self.assertEqual(self.order.total_price, 150000)

class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', password='rimpmpass90')
        self.category = Category.objects.create(name="Гитары")
        self.product = Product.objects.create(
            name="Jackson Stars Soloist SL7-J2B",
            price=150000,
            stock=2,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=150000,
            delivery_address="ул. Пушкина, д. 10",
            phone="+7 999 123-45-67"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price_at_time=150000,
            total_price=150000
        )

    def test_get_orders_unauthorized(self):
        response = self.client.get('/api/orders/orders/')
        self.assertEqual(response.status_code, 401)

    def test_get_orders_authorized(self):
        access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/orders/orders/')
        self.assertEqual(response.status_code, 200)