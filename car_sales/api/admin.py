from django.contrib import admin

from api import models

admin.site.register(models.CustomUser)
admin.site.register(models.CarBrand)
admin.site.register(models.CarType)
admin.site.register(models.CarModel)
admin.site.register(models.Car)
