from rest_framework import serializers

from api.constants import model_types
from api.models import CarType


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    model_type = serializers.ChoiceField(
        choices=model_types.MODEL_TYPE_CHOICES,
    )

    class Meta:
        fields = ["file_uploaded", "model_type"]


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = "__all__"
