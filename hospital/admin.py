from django.contrib import admin
from hospital.models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Product)
admin.site.register(Doctor)
admin.site.register(Location)
admin.site.register(Connection)
admin.site.register(Worker)