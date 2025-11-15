# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Department, Doctor, Patient, Appointment,
    MedicalRecord, InventoryItem
)
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ["user", "role"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(write_only=True)
    user_email = serializers.EmailField(write_only=True)

    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "email",
            "specialization",
            "experience",
            "phone",
            "availability",
            "patients",
            "rating",
            "user_name",
            "user_email",
        ]
        read_only_fields = ["id"]

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()

    def get_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        name = validated_data.pop("user_name")
        email = validated_data.pop("user_email")

        parts = name.split(" ")
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        return Doctor.objects.create(user=user, **validated_data)


class PatientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id", "first_name", "last_name", "name", "age", "dob",
            "gender", "phone", "email", "address", "blood_type",
            "last_visit", "status", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_age(self, obj):
        return obj.age


class AppointmentSerializer(serializers.ModelSerializer):
    patientName = serializers.SerializerMethodField()
    doctorName = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), allow_null=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "patient", "patientName", "doctor", "doctorName",
            "scheduled_at", "date", "time", "type", "reason", "status", "created_at"
        ]
        read_only_fields = ["created_at"]

    def get_patientName(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def get_doctorName(self, obj):
        if obj.doctor and obj.doctor.user:
            return obj.doctor.user.get_full_name()
        elif obj.doctor:
            return str(obj.doctor)
        return None

    def get_date(self, obj):
        return obj.scheduled_at.date().isoformat()

    def get_time(self, obj):
        return obj.scheduled_at.time().strftime("%I:%M %p")  # "09:00 AM"


class MedicalRecordSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = MedicalRecord
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    needs_reorder = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = [
            "id", "sku", "name", "category", "uses",
            "stock", "min_stock", "unit", "expiry_date",
            "needs_reorder", "created_at", "updated_at"
        ]

    def get_needs_reorder(self, obj):
        return obj.needs_reorder()
