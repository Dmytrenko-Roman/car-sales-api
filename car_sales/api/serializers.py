from rest_framework import serializers

from api import constants


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    model_type = serializers.ChoiceField(
        choices=constants.MODEL_TYPE_CHOICES,
    )

    class Meta:
        fields = ["file_uploaded", "model_type"]
