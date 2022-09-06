from rest_framework import serializers

from api.constants import model_types


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    model_type = serializers.ChoiceField(
        choices=model_types.MODEL_TYPE_CHOICES,
    )

    class Meta:
        fields = ["file_uploaded", "model_type"]
