from rest_framework.serializers import ValidationError


def validate_phone_number(phone_number):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']

    if not phone_number[0] in ['0', '+']:
        raise ValidationError("Invalid phone number. Please, enter a valid phone number.")
    for number in phone_number[1:]:
        if number not in numbers:
            raise ValidationError("Invalid phone number. Please, enter a valid phone number.")