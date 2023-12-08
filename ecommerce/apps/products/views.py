from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer
from ..carts.models import Cart, Item


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        user = request.user
        quantity = int(request.data["quantity"])
        product = Product.objects.get(pk=pk)
        cart, created = Cart.objects.get_or_create(user=user, is_purchased=False)
        cart_item, created = Item.objects.get_or_create(cart=cart, product=product)
        if created: quantity -= 1
        cart_item.quantity += quantity
        cart_item.save()
        return Response(data={'status': 'success'}, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser()]
        else:
            permission_classes = [permission for permission in super().get_permissions()]
        return [permission for permission in permission_classes]
