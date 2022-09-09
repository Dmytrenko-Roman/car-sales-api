from rest_framework import status, viewsets
from rest_framework.response import Response

from api.constants.model_types import MODEL_TYPES
from api.serializers import (
    UploadSerializer,
    CarTypeSerializer,
    CarBrandSerializer,
    CarModelSerializer,
    CarSerializer,
)
from api.utils import parser
from api.models import CarType, CarBrand, CarModel, Car


class CarTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CarTypeSerializer
    queryset = CarType.objects.all()


class CarBrandViewSet(viewsets.ModelViewSet):
    serializer_class = CarBrandSerializer
    queryset = CarBrand.objects.all()


class CarModelViewSet(viewsets.ModelViewSet):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


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
            MODEL_TYPES[model_type].objects.bulk_create(
                data, ignore_conflicts=True
            )
        except Exception:
            return Response(
                {
                    "detail": "Invalid values for fields.",
                    "model_type": model_type,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": f"{model_type} objects was successfully created."},
            status=status.HTTP_201_CREATED,
        )
