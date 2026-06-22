from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, product_detail
from .views import FilterViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'filters', FilterViewSet)

urlpatterns = [
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('', include(router.urls)),
]
