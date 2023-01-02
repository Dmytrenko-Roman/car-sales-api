from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from api.constants.model_types import MODEL_TYPES
from api.models import Car, CarBrand, CarModel, CarType, CustomUser
from api.serializers import (
    CarBrandSerializer,
    CarModelSerializer,
    CarSerializer,
    CarTypeSerializer,
    CustomUserSerializer,
    UploadSerializer,
    RegisterSerializer,
)
from api.utils import parser
from api.permissions import (
    AllowGetRetrieve,
    AllowCreate,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    default_serializer_class = CustomUserSerializer
    serializer_classes = {
        "create": RegisterSerializer,
    }

    permission_classes = [IsAdminUser | AllowCreate]

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class
        )

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def profile(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data)

    @action(
        detail=False, methods=["put"], permission_classes=[IsAuthenticated]
    )
    def update_profile(self, request):
        user = request.user
        data = request.data
        serializer = RegisterSerializer(user, many=False)

        user.username = data["username"]
        user.email = data["email"]
        user.phone_number = data["phone_number"]
        user.subscription = data["subscription"]
        if data["password"] != "":
            user.password = make_password(data["password"])
        user.save()

        return Response(serializer.data)


class CarTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CarTypeSerializer
    queryset = CarType.objects.all()
    permission_classes = [IsAdminUser | AllowGetRetrieve]


class CarBrandViewSet(viewsets.ModelViewSet):
    serializer_class = CarBrandSerializer
    queryset = CarBrand.objects.all()
    permission_classes = [IsAdminUser | AllowGetRetrieve]


class CarModelViewSet(viewsets.ModelViewSet):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()
    permission_classes = [IsAdminUser | AllowGetRetrieve]


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated | AllowGetRetrieve]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["model"]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def destroy(self, request, pk=None):
        car = Car.objects.get(pk=pk)
        if request.user.id != car.owner_id:
            return Response(
                {"message": "You do not have permission to do this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
