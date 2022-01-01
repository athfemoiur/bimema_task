from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'confirm_password')

    def validate(self, attrs):
        validate_password(attrs.get('password'))
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError('Password and Confirm Password are not equal!')

        return attrs

    @staticmethod
    def clean_validated_data(validated_data):
        validated_data.pop('confirm_password')
        return validated_data

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**self.clean_validated_data(validated_data))
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        refresh_token = RefreshToken.for_user(instance)
        access_token = refresh_token.access_token

        return {
            **ret,
            'access_token': str(access_token),
            'refresh_token': str(refresh_token)
        }


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone_number')


class UserChangePasswordSerializer(ModelSerializer):
    old_password = CharField(write_only=True, required=True)
    new_password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        validate_password(attrs.get('new_password'))
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise ValidationError('Password and Confirm Password are not equal!')

        return attrs

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get('old_password')):
            instance.password = make_password(validated_data.get('new_password'))
            instance.save()
            return instance
        raise ValidationError('Old password is not correct!')
