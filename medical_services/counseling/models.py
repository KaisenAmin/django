from django.db import models
from django.conf import settings
# from core.models import Clinic, Hospital
# from users.doctor.models import Doctor

class Weekday(models.Model):
    day = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.day


class CounselingSession(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='counseling_sessions')
    counselor = models.ForeignKey("Doctor", on_delete=models.SET_NULL, null=True, related_name='counseling_provided')
    clinic = models.ForeignKey("Clinic", on_delete=models.CASCADE, related_name='counseling_sessions', blank=True, null=True)
    hospital = models.ForeignKey("Hospital", on_delete=models.CASCADE, related_name='counseling_sessions', blank=True, null=True)
    
    service_days = models.ManyToManyField(Weekday, related_name='counseling_sessions')
    start_time = models.TimeField(help_text="Start time for the service on the specified days")
    end_time = models.TimeField(help_text="End time for the service on the specified days")
    
    number_of_sessions = models.PositiveIntegerField(help_text="Total number of sessions for the counseling", default=1)
    session_duration = models.PositiveIntegerField(help_text="Duration of each session in minutes")
    session_type = models.CharField(max_length=100, choices=[('online', 'Online'), ('in-person', 'In-person')])
    date = models.DateField(help_text="Start date of the first session")
    time = models.TimeField(help_text="Start time of the first session")
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total cost for all the sessions")
    
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Counseling session for {self.patient.username} on {self.date} at {self.time}"
