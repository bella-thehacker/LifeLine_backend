from django.contrib import admin

# Register your models here.

from .models import Department, Doctor, Patient, Appointment, MedicalRecord

admin.site.register([Department, Doctor, Patient, Appointment, MedicalRecord])