import uuid

from django.db import models


# Create your models here.

class Doctor(models.Model):
    national_id = models.CharField(max_length=40, primary_key=True, editable=False)
    name = models.CharField(max_length=255, default="")

class Patient(models.Model):
    national_id = models.CharField(max_length=40, primary_key=True, editable=False)
    name = models.CharField(max_length=255, default="")

class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    drugs_list = models.CharField(max_length=255, default="")
    comment = models.CharField(max_length=255, default="", blank=True)
    created = models.DateTimeField(auto_now=True)