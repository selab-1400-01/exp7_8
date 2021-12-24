import uuid

from django.db import models


# Create your models here.

class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_national_id = models.CharField(max_length=40, db_index=True, editable=False)
    doctor_national_id = models.CharField(max_length=40, db_index=True, editable=False)
    drugs_list = models.CharField(max_length=255, default="")
    comment = models.CharField(max_length=255, default="", blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'main'
