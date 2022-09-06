from api.models import CarBrand, CarModel, CarType

MODEL_TYPES = {
    "car_brand": CarBrand,
    "car_model": CarModel,
    "car_type": CarType,
}

MODEL_TYPE_CHOICES = (
    ("car_brand", "Car Brand"),
    ("car_model", "Car Model"),
    ("car_type", "Car Type"),
)
