from django.db import models
# from app.users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# from .models import Patient
# from ..models import Address
from enum import Enum


class GenderType(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'

class DoctorStatus(models.TextChoices):
    AVAILABLE = 'AV', 'Available'
    ON_BREAK = 'OB', 'On Break'
    OFFLINE = 'OF', 'Offline'

class AppointmentStatus(models.TextChoices):
    PENDING = 'P', 'Pending'
    CONFIRMED = 'C', 'Confirmed'
    CANCELED = 'X', 'Canceled'


class WeeklyHours(models.Model):
    monday_start = models.TimeField(verbose_name="Monday Start Time")
    monday_end = models.TimeField(verbose_name="Monday End Time")

    tuesday_start = models.TimeField(verbose_name="Tuesday Start Time")
    tuesday_end = models.TimeField(verbose_name="Tuesday End Time")

    wednesday_start = models.TimeField(verbose_name="Wednesday Start Time")
    wednesday_end = models.TimeField(verbose_name="Wednesday End Time")

    thursday_start = models.TimeField(verbose_name="Thursday Start Time")
    thursday_end = models.TimeField(verbose_name="Thursday End Time")

    friday_start = models.TimeField(verbose_name="Friday Start Time")
    friday_end = models.TimeField(verbose_name="Friday End Time")

    saturday_start = models.TimeField(verbose_name="Saturday Start Time")
    saturday_end = models.TimeField(verbose_name="Saturday End Time")

    sunday_start = models.TimeField(verbose_name="Sunday Start Time")
    sunday_end = models.TimeField(verbose_name="Sunday End Time")


class CallType(Enum):
    VOICE = 'voice'
    VIDEO = 'video'


class CallStatus(Enum):
    MISSED = 'missed'
    REJECTED = 'rejected'
    SUCCESSFUL = 'successful'


class Call(models.Model):
    callId = models.AutoField(primary_key=True)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    callDate = models.DateField()  # Added this line for the call date
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    callType = models.CharField(
        max_length=10, 
        choices=[(tag, tag.value) for tag in CallType]
    )
    callStatus = models.CharField(
        max_length=15, 
        choices=[(tag, tag.value) for tag in CallStatus]
    )


class Message(models.Model):
    messageId = models.AutoField(primary_key=True)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    sender = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Doctor(models.Model):
    doctorId = models.AutoField(primary_key=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    licenseNumber = models.CharField(max_length=255)
    isRegistered = models.BooleanField(default=False)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GenderType.choices)
    status = models.CharField(max_length=2, choices=DoctorStatus.choices)
    availableHours = models.OneToOneField(WeeklyHours, on_delete=models.CASCADE)

    # Associations
    # Since 'Appointment', 'MedicalService', and 'Package' have ManyToMany relations with 'Doctor', 
    # they should be defined in their respective models.
    office_address = models.OneToOneField("OfficeAddress", on_delete=models.CASCADE, related_name='doctor')
    personal_address = models.OneToOneField("Address", on_delete=models.CASCADE, related_name='doctor_personal_address')

class Appointment(models.Model):
    appointmentId = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey("User", on_delete=models.CASCADE, related_name='appointments_as_patient')  # Assuming Patient is a User
    appointmentDate = models.DateField()  # Added this line for the appointment date
    appointmentTime = models.DateTimeField()
    appointmentStatus = models.CharField(max_length=1, choices=AppointmentStatus.choices)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    # Associations
    services = models.ManyToManyField("MedicalService", blank=True, related_name='appointments')
    calls = models.ManyToManyField('Call', blank=True)
    messages = models.ManyToManyField('Message', blank=True)
  




class MedicalService(models.Model):
    serviceId = models.AutoField(primary_key=True)
    serviceName = models.CharField(max_length=255)
    serviceDescription = models.TextField(blank=True)
    price = models.FloatField()
    # Associations
    doctors = models.ManyToManyField(Doctor, related_name='services')
    packages = models.ManyToManyField("Package", blank=True, related_name='services') # changed from "services" to "packages" for clarity
    # We'll add the association with Appointment in the Appointment model itself


class Package(models.Model):
    packageId = models.AutoField(primary_key=True)
    packageName = models.CharField(max_length=255)
    packageDescription = models.TextField(blank=True)
    price = models.FloatField()
    # Associations
    doctors = models.ManyToManyField(Doctor, related_name='packages')
    services = models.ManyToManyField(MedicalService, related_name='included_in_packages') # changed related_name for clarity
    # The association with Discount is presumed to be set up in the Discount model


class Review(models.Model):
    # Attributes:
    reviewId = models.AutoField(primary_key=True)  # Review ID as the primary key
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating, ranging from 1 to 5
    comment = models.TextField()  # Comment as a textual description
    
    # Associations:
    # A review is associated with one Doctor. 
    # The related_name 'reviews' means we can access all reviews of a Doctor using doctor_instance.reviews.all()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')  
    
    # A review is written by one User.
    # The related_name 'reviews_given' allows us to access all reviews given by a User using user_instance.reviews_given.all()
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='reviews_given')


class Discount(models.Model):
    # Attributes:
    discountId = models.AutoField(primary_key=True)      # Discount ID as the primary key
    discountValue = models.FloatField()                  # The amount or percentage of the discount
    discountCode = models.CharField(max_length=255)      # The code that might be used to apply the discount
    startDate = models.DateTimeField()                    # Start date of the discount validity
    endDate = models.DateTimeField()                     # End date of the discount validity
    
    # Associations:
    
    # Each discount can be applied to multiple Packages.
    # If you want to access all discounts for a specific package, you can use package_instance.discounts.all()
    packages = models.ManyToManyField(Package, related_name='discounts', blank=True)  
    
    # Each discount can be applied to multiple Medical Services.
    # Similarly, for a specific medical service, you can use medical_service_instance.discounts.all()
    services = models.ManyToManyField(MedicalService, related_name='discounts', blank=True)


class OfficeAddress(models.Model):
    # Attributes:
    
    # Unique identifier for each office address
    addressId = models.AutoField(primary_key=True)
    
    # Address details
    street = models.CharField(max_length=255)         # Street information
    city = models.CharField(max_length=255)           # City information
    state = models.CharField(max_length=255)          # State or province information
    country = models.CharField(max_length=255)        # Country information
    zipCode = models.CharField(max_length=10)         # ZIP or postal code
    
    # Associations:
    
    # Each office address is associated with one doctor.
    # This implies that a doctor can only have one office address, which seems logical.
    # If you wanted to get the office address for a doctor, you could use doctor_instance.office_address
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name='office_address')