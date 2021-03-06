# Generated by Django 3.2 on 2021-12-31 14:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='LifeInsurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex='09\\d{9}')])),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(45)])),
                ('bmi', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(0)])),
                ('cigarette', models.BooleanField()),
                ('hookah', models.BooleanField()),
                ('cigarette_number', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('hookah_number', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='life_insurances', to='insurance.branch')),
            ],
        ),
    ]
