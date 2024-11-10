
# Create your models here.
from django.db import models
from django.utils import timezone

class Patient(models.Model):
    patient_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.patient.name} on {self.appointment_date}"
    
class Product(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)  # e.g., Medication, Treatment, etc.
    created_at = models.DateTimeField(default= timezone.now)
    def __str__(self): 
        return self.name
    

class Voucher(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Voucher for {self.patient.name} on {self.created_at.date()}"


class MedicalPayment(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, default=1)
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    def __str__(self): 
        return f"Payment of {self.amount} for Voucher {self.voucher.id} - {'Paid' if self.is_paid else 'Unpaid'}"

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)        # Doctor's first name
    last_name = models.CharField(max_length=100)         # Doctor's last name
    age = models.IntegerField(null=True, blank=True)     # Doctor's age (optional)
    specialty = models.CharField(max_length=100)         # Area of specialty (e.g., Cardiology, Pediatrics)
    phone_number = models.CharField(max_length=15, blank=True)  # Contact number (optional)
    email = models.EmailField(blank=True)                # Email address (optional)
    address = models.TextField(blank=True)               # Address (optional)
    years_of_experience = models.IntegerField(null=True, blank=True)  # Years of experience
    created_at = models.DateTimeField(default=timezone.now)  # Date added to the system

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialty}"
    
class Worker(models.Model):
    first_name = models.CharField(max_length=100)        # Doctor's first name
    last_name = models.CharField(max_length=100)         # Doctor's last name
    age = models.IntegerField(null=True, blank=True)     # Doctor's age (optional)
    specialty = models.CharField(max_length=100)         # Area of specialty (e.g., Cardiology, Pediatrics)
    phone_number = models.CharField(max_length=15, blank=True)  # Contact number (optional)
    email = models.EmailField(blank=True)                # Email address (optional)
    address = models.TextField(blank=True)               # Address (optional)
    years_of_experience = models.IntegerField(null=True, blank=True)  # Years of experience
    created_at = models.DateTimeField(default=timezone.now)  # Date added to the system

    def __str__(self):
        return f"MR/MRS {self.first_name} {self.last_name} - {self.specialty}"    
    
# For the shortest path algorithm
class Location(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Connection(models.Model):
    start = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="outgoing_connections")
    end = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="incoming_connections")
    distance = models.FloatField()  # Distance or travel time in kilometers or minutes
    def __str__(self):
        return f"{self.start} to {self.end} - {self.distance} units"

