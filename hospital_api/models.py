# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

ROLE_CHOICES = [
    ("admin", "Admin"),
    ("staff", "Staff"),
    ("doctor", "Doctor"),
]

AVAILABILITY_CHOICES = [
    ("available", "Available"),
    ("unavailable", "Unavailable"),
    ("on_leave", "On Leave"),
]

APPOINTMENT_STATUS = [
    ("scheduled", "Scheduled"),
    ("confirmed", "Confirmed"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255, blank=True)
    experience = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    availability = models.CharField(max_length=20, default="available")
    rating = models.FloatField(default=0.0)
    patients = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Patient(models.Model):
    # keep first_name + last_name for normalization, expose full name in serializer
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    last_visit = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, default="active")  # e.g., active, inactive

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        if not self.dob:
            return None
        today = timezone.localdate()
        age = today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )
        return age


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, related_name="appointments"
    )
    scheduled_at = models.DateTimeField()
    type = models.CharField(max_length=150, blank=True)  # e.g., "Cardiology Checkup"
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"{self.patient} with {self.doctor} at {self.scheduled_at}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="records"
    )
    notes = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient} at {self.created_at}"


class InventoryItem(models.Model):
    # medicines / consumables
    sku = models.CharField(max_length=50, unique=True)  # e.g., "M001"
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=150, blank=True)
    uses = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, blank=True)  # e.g., "tablets", "bottles"
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def needs_reorder(self):
        return self.stock <= self.min_stock

    def __str__(self):
        return f"{self.name} ({self.sku})"
