from django.urls import path

from insurance.views import LifeInsuranceCreateView

app_name = 'insurance'

urlpatterns = [
    path('life-insurance/', LifeInsuranceCreateView.as_view(), name='life-insurance')
]
