from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from insurance.serializers import LifeInsuranceSerializer


class LifeInsuranceCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LifeInsuranceSerializer
