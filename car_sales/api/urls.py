from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"upload", views.UploadViewSet, basename="upload")
router.register(r"cartypes", views.CarTypeViewSet, basename="car_type")
router.register(r"carbrands", views.CarTypeViewSet, basename="car_brands")

urlpatterns = [
    path("", include(router.urls)),
]
