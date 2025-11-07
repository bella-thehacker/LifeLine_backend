from rest_framework import routers
from django.urls import path, include
from .views import PatientViewSet, DoctorViewSet, AppointmentViewSet, DepartmentViewSet, MedicalRecordViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'records', MedicalRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]