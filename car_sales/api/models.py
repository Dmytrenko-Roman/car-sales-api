from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class CarType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=30)

    type = models.ForeignKey(to=CarType, on_delete=models.CASCADE, null=False)
    brand = models.ForeignKey(
        to=CarBrand, on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        return f"{self.brand} {self.name}"
