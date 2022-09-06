from rest_framework import status, viewsets
from rest_framework.response import Response

from api.constants import MODEL_TYPES
from api.serializers import UploadSerializer
from api.utils import parser


class UploadViewSet(viewsets.ViewSet):
    serializer_class = UploadSerializer

    def create(self, request):
        file_obj = request.data["file_uploaded"]
        model_type = request.data["model_type"]
        if (
            isinstance(file_obj, str)
            or file_obj._name.split(".")[-1] != "xlsx"
        ):
            msg = {"detail": "File is invalid."}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = [
                MODEL_TYPES[model_type](**row)
                for row in parser.parse_data(file_obj.file)
            ]
            MODEL_TYPES[model_type].objects.bulk_create(data)
        except Exception:
            return Response(
                {
                    "detail": "Invalid values for fields.",
                    "model_type": model_type,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Oil objects was successfully created."},
            status=status.HTTP_201_CREATED,
        )
