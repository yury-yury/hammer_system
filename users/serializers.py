from typing import Dict, Any

from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from hammer_system_2 import settings
from users.models import User, CallbackToken
from users.utils import generate_referral_code


class LoginSerializer(serializers.ModelSerializer):
    """
    The LoginSerializer class inherits from the ModelSerializer class from the rest_framework.serializers module.
    Designed to serialize and deserialize objects when making requests to the LoginView.
    """
    phone = PhoneNumberField(required=True)

    class Meta:
        model = User
        read_only_fields = ("id", )
        fields = ("id", "phone")

    def create(self, validated_data: dict) -> User:
        """
        The create function overrides the base class method. Retrieves the user object from the database,
        creates it if it does not exist. Produces the creation of a 4-digit digital token for authentication.
        Returns a user object.
        """
        instance, _ = User.objects.get_or_create(**validated_data)

        if instance.referral_code == None:
            instance.referral_code = generate_referral_code()
            instance.save()

        token = CallbackToken.objects.create(user=instance)
        token.save()

        return instance


class TokenField(serializers.CharField):
    """
    The TokenField class extends the CharField serializer field class from the rest_framework.serializers module.
    """
    default_error_messages = {
        'required': 'Invalid Token',
        'invalid': 'Invalid Token',
        'blank': 'Invalid Token',
        'max_length': 'Tokens are {max_length} digits long.',
        'min_length': 'Tokens are {min_length} digits long.'
    }


def token_age_validator(token) -> bool:
    """
    The function token_age_validator is a validator for checking the age of use of a futification proof token.
    It accepts the value of a token as parameters. At the end of the term of use of the token, it invalidates it.
    Returns True if the token is valid, otherwise False.
    """
    try:
        callback_token = CallbackToken.objects.filter(key=token, is_active=True).first()
        seconds = (timezone.now() - callback_token.created_at).total_seconds()
        if seconds <= settings.TOKEN_EXPIRE_TIME:
            return True
        else:
            # Invalidate our token.
            callback_token.is_active = False
            callback_token.save()
            return False

    except CallbackToken.DoesNotExist:
        # No valid token.
        return False


class VerifyTokenSerializer(serializers.Serializer):
    """
    The VerifyTokenSerializer class inherits from the Serializer class from the rest_framework.serializers module.
    Designed to serialize and deserialize objects when processing a request for a VerifyTokenView.
    """
    phone = PhoneNumberField(required=False, max_length=17)
    token = TokenField(min_length=4, max_length=4, validators=[token_age_validator])

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        The validate function overrides a class method. It takes as parameters an object in the form of a dictionary.
        Performs validation of the received data, supplements them and returns them as a dictionary.
        """
        try:
            callback_token = attrs.get('token', None)
            phone = attrs.get('phone', None)
            user = User.objects.get(phone=phone)
            CallbackToken.objects.filter(user=user, key=callback_token, is_active=True).first()
            attrs['user'] = user
            user.is_verified = True
            user.save()

            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')

        except CallbackToken.DoesNotExist:
            raise serializers.ValidationError('Invalid entered token')
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid user provided.')
        except ValidationError:
            raise serializers.ValidationError('Invalid parameters provided.')
        else:
            return attrs


class TokenResponseSerializer(serializers.Serializer):
    """
    The TokenResponseSerializer class inherits from the parent Serializer class
    from the rest_framework.serializers module.
    Represents a serializer for convenient serialization and deserialization of objects of the Token class.
    """
    token = serializers.CharField(source='key')
    key = serializers.CharField(write_only=True)


class ProfileForeignSerializer(serializers.ModelSerializer):
    """
    The ProfileForeignSerializer class is designed to conveniently provide data from related models.
    Inherited from the ModelSerializer class from the rest_framework.serializers module.
    """
    class Meta:
        model = User
        fields = ['phone', ]


class ProfileSerializer(serializers.ModelSerializer):
    """
    The ProfileSerializer class is a serializer for convenient serialization and deserialization of objects
    when making requests to the ProfileView using the GET and PATCH methods.
    Inherited from the ModelSerializer class from the rest_framework.serializers module.
    """
    other_referral_code = serializers.CharField(write_only=True)
    entered_referral_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'phone', 'referral_code', 'first_name', 'last_name',
                  'email', 'other_referral_code', 'entered_referral_code']

    def get_entered_referral_code(self, obj):
        queryset = User.objects.filter(else_referral_code=obj)
        return [ProfileForeignSerializer(q).data for q in queryset]

    def is_valid(self, *, raise_exception=False):
        else_referral_code = self.initial_data.get('other_referral_code', None)
        if else_referral_code is not None:
            if self.instance.else_referral_code is not None:
                raise serializers.ValidationError('You can activate the invite code only once.')
            else:
                try:
                    else_user = User.objects.get(referral_code=else_referral_code)
                except User.DoesNotExist:
                    raise serializers.ValidationError('Incorrect code entered.')
                else:
                    self.instance.else_referral_code = else_user
                    self.instance.save()

        super().is_valid(raise_exception=raise_exception)
