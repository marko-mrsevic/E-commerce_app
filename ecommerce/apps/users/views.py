from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from .permissions import IsOwnerOrAdminUser
from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=IsOwnerOrAdminUser)
    def register_user(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == "register_user":
            permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdminUser]
        else:
            permission_classes = [permission for permission in super().get_permissions()]
        return [permission() for permission in permission_classes]
