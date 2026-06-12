from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Bike)
admin.site.register(Laptop)
admin.site.register(Camera)

admin.site.register(BikeBooking)
admin.site.register(LaptopBooking)
admin.site.register(CameraBooking)