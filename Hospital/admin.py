from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Laboratory)
admin.site.register(Billing)
admin.site.register(LabTest)
admin.site.register(CareerApply)
admin.site.register(DoctorAppointment)