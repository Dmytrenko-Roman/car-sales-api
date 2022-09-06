from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants.car_fields import ENGINE_TYPE_CHOICES


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class CarType(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=30, null=False)

    type = models.ForeignKey(to=CarType, on_delete=models.CASCADE, null=False)
    brand = models.ForeignKey(
        to=CarBrand, on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f"{self.brand} {self.name}"


class Car(models.Model):
    price = models.PositiveIntegerField(null=False)
    mileage = models.PositiveIntegerField(null=False)
    year = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=500, null=True)
    engine_volume = models.DecimalField(
        max_digits=2, decimal_places=1, default=0
    )
    engine_type = models.CharField(max_length=20, choices=ENGINE_TYPE_CHOICES, null=True)
    horsepower = models.PositiveIntegerField(null=False)
    # TODO: add color field
    owners_count = models.PositiveIntegerField(default=1)
    seats_count = models.PositiveIntegerField(null=False)
    doors_count = models.PositiveIntegerField(null=False)

    model = models.ForeignKey(
        to=CarModel, on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f"{str(self.model)}: ${str(self.price)}"
