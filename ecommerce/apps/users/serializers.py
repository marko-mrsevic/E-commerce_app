from rest_framework import serializers
from .models import User, Address
from .validators import validate_phone_number


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_phone_number])

    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code', 'phone']

    def create(self, validated_data):
        user = self.context['user']

        address = Address.objects.create(user=user, **validated_data)
        return address
