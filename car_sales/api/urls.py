from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"upload", views.UploadViewSet, basename="upload")

urlpatterns = [
    path("", include(router.urls)),
]
