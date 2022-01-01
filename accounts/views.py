from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsNotAuthenticated
from accounts.serializers import UserRegistrationSerializer, UserInfoSerializer, UserChangePasswordSerializer

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    """
    Register the user with username, phone_number, password
    with required validations
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsNotAuthenticated,)


class UserInfoView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class UserChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response('Password has been changed successfully')
