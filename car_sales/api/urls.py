from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api import views

router = routers.DefaultRouter()
router.register(r"upload", views.UploadViewSet, basename="upload")
router.register(r"cartypes", views.CarTypeViewSet, basename="car_type")
router.register(r"carbrands", views.CarBrandViewSet, basename="car_brands")
router.register(r"carmodels", views.CarModelViewSet, basename="car_models")
router.register(r"cars", views.CarViewSet, basename="cars")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]
