import stripe
from rest_framework import viewsets
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwnerOrAdminUser, IsOwner
from .models import Cart, Order
from .serializers import CartSerializer
from ..users.serializers import AddressSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsOwner])
    def make_payment(self, request, pk=None):
        serializer = AddressSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(pk=pk)
            amount = cart.total_price()
            amount = int(amount * 100)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                payment_method="pm_card_visa"
            )

            client_secret = intent.client_secret

            cart.is_purchased = True
            cart.save()
            order = Order(cart=cart)
            order.save()

            return Response(data={'client_secret': client_secret}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({str(e)})

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser()]
        elif self.action in ['retrieve', 'create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdminUser()]
        else:
            permission_classes = [permission for permission in super().get_permissions()]
        return [permission for permission in permission_classes]
