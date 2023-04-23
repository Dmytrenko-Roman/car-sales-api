from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.constants import model_types
from api.models import Car, CarBrand, CarModel, CarType, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "subscription",
            "image_url",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "phone_number",
            "subscription",
            "token",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            subscription=validated_data["subscription"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)

        return str(token.access_token)


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = "__all__"


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"


class CarBrandSerializer(serializers.ModelSerializer):
    models = CarModelSerializer(many=True, read_only=True)

    class Meta:
        model = CarBrand
        fields = ("id", "name", "models")


class CarSerializer(serializers.ModelSerializer):
    model = CarModelSerializer(read_only=True)
    owner = CustomUserSerializer(read_only=True)
    engine_type = serializers.CharField(source="get_engine_type_display")
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Car
        fields = "__all__"
        extra_kwargs = {
            "owner": {"read_only": True},
        }


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    model_type = serializers.ChoiceField(
        choices=model_types.MODEL_TYPE_CHOICES,
    )

    class Meta:
        fields = ["file_uploaded", "model_type"]
