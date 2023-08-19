from django.db import models
# from users.models import User

class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name='patient_profile')
    healthRecord = models.TextField(blank=True)
    
    # If you have an Appointment model elsewhere, ensure the relationship is set.
    # The ForeignKey in the Appointment model pointing to this Patient model
    # will automatically set up the reverse relation as 'appointment_set' by default.
    # However, you can give it a custom name using the 'related_name' attribute.
    # For example, in the Appointment model:
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
