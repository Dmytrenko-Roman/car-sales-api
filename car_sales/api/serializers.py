from rest_framework import serializers

from api.constants import model_types
from api.models import CarType, CarBrand, CarModel, Car, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "phone_number", "subscription"]


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = "__all__"


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = "__all__"


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    model_type = serializers.ChoiceField(
        choices=model_types.MODEL_TYPE_CHOICES,
    )

    class Meta:
        fields = ["file_uploaded", "model_type"]
