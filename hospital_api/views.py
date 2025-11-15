from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, Doctor, Appointment, Department, MedicalRecord
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer, DepartmentSerializer, MedicalRecordSerializer
from .models import InventoryItem
from .serializers import InventoryItemSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all().order_by("name")
    serializer_class = InventoryItemSerializer

    # GET /inventory/low-stock/
    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        low_stock_items = InventoryItem.objects.filter(stock__lte=models.F("min_stock"))
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

    # GET /inventory/summary/
    @action(detail=False, methods=["get"])
    def summary(self, request):
        total_medicines = InventoryItem.objects.count()
        total_units = InventoryItem.objects.all().values_list("stock", flat=True)

        return Response({
            "total_medicines": total_medicines,
            "total_units": sum(total_units)
        })