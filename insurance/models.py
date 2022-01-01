from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Manager


class Branch(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class LifeInsuranceManager(Manager):

    def create(self, **data):
        if not data['cigarette']:
            data['cigarette_number'] = 0
        if not data['hookah']:
            data['hookah_number'] = 0
        instance = self.model(**data)
        instance.save(using=self._db)
        return instance


class LifeInsurance(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(regex=r"09\d{9}")])
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(45)])
    bmi = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0)])
    cigarette = models.BooleanField()
    hookah = models.BooleanField()
    cigarette_number = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    hookah_number = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    branch = models.ForeignKey(Branch, related_name='life_insurances', on_delete=models.PROTECT)

    objects = LifeInsuranceManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
