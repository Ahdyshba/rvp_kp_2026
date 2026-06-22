from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return Order.objects.all()
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        order = serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None
        )

        cart = None
        
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        
        if cart:
            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_time=cart_item.product.price,
                    total_price=cart_item.product.price * cart_item.quantity
                )
            cart.cartitem_set.all().delete()

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]