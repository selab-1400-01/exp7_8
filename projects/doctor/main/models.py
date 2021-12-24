import uuid

from django.db import models


# Create your models here.

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    national_id = models.CharField(max_length=40, db_index=True, unique=True, editable=False)
    name = models.CharField(max_length=255, default="")
    created = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'main'
