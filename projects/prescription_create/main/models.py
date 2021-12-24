from django.db import models

# Create your models here.

class PatientId(models.Model):
    national_id = models.CharField(primary_key=True, max_length=40, editable=False)