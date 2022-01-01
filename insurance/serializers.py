from rest_framework.serializers import ModelSerializer

from insurance.models import LifeInsurance


class LifeInsuranceSerializer(ModelSerializer):
    class Meta:
        model = LifeInsurance
        fields = '__all__'

