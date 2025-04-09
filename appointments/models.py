from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    available = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.name} - {self.specialization}"

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    symptoms = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    urgency_score = models.IntegerField(default=0)
    date = models.DateField()  # 🗓️ Appointment date
    time = models.TimeField()  # ⏰ Appointment time

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.time}"

class TriageForm(models.Model):
    symptom1 = models.BooleanField(default=False)
    symptom2 = models.BooleanField(default=False)
    symptom3 = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin')
    ])
