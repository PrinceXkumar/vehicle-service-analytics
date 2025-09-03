from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Profile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_MECHANIC = 'mechanic'
    ROLE_CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MANAGER, 'Service Manager'),
        (ROLE_MECHANIC, 'Mechanic'),
        (ROLE_CUSTOMER, 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    vin = models.CharField(max_length=64, unique=True)
    registration_number = models.CharField(max_length=32, unique=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration_number} - {self.make} {self.model}"

class ServiceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='services')
    service_date = models.DateField(default=timezone.now)
    odometer_reading = models.PositiveIntegerField(help_text="Odometer at service time (km)")
    issues_reported = models.TextField(blank=True, null=True)
    work_done = models.TextField(blank=True, null=True)
    parts_replaced = models.TextField(blank=True, null=True, help_text="Comma-separated list or JSON later")
    parts_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    mechanic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='performed_services')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return (self.parts_cost or 0) + (self.labor_cost or 0)

    def __str__(self):
        return f"Service on {self.service_date} for {self.vehicle.registration_number}"


class Service(models.Model):
    SERVICE_OIL_CHANGE = 'oil_change'
    SERVICE_TYRE_REPLACEMENT = 'tyre_replacement'
    SERVICE_BRAKE_INSPECTION = 'brake_inspection'
    SERVICE_GENERAL_CHECKUP = 'general_checkup'

    SERVICE_TYPE_CHOICES = [
        (SERVICE_OIL_CHANGE, 'Oil Change'),
        (SERVICE_TYRE_REPLACEMENT, 'Tyre Replacement'),
        (SERVICE_BRAKE_INSPECTION, 'Brake Inspection'),
        (SERVICE_GENERAL_CHECKUP, 'General Checkup'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_services')
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    assigned_mechanic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_services')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.get_status_display()}"