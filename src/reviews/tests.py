from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import Review
from catalog.models import Product, Category

User = get_user_model()

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', password='rimpmpass90')
        self.category = Category.objects.create(name="Гитары")
        self.product = Product.objects.create(
            name="SCHECTER PT SPECIAL",
            price=80000,
            stock=3,
            category=self.category
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            text="Отличная гитара, звук супер!"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.product.name, "SCHECTER PT SPECIAL")
        self.assertEqual(self.review.user.username, "useruser")
        self.assertEqual(self.review.rating, 5)

class ReviewAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='useruser', password='rimpmpass90')
        self.category = Category.objects.create(name="Гитары")
        self.product = Product.objects.create(
            name="Ibanez RGA7",
            price=70000,
            stock=5,
            category=self.category
        )

    def test_get_reviews_unauthorized(self):
        response = self.client.get('/api/reviews/reviews/')
        self.assertEqual(response.status_code, 401)

    def test_get_reviews_authorized(self):
        access_token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/reviews/reviews/')
        self.assertEqual(response.status_code, 200)