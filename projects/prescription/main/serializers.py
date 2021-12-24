from rest_framework import serializers
from main.models import Prescription


class PrescriptionSerializer(serializers.Serializer):
    patient_national_id = serializers.CharField(max_length=40)
    doctor_id = serializers.CharField(max_length=40)
    drugs_list = serializers.CharField(max_length=255, default="")
    comment = serializers.CharField(max_length=255, allow_blank=True, default="")

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data):
        return Prescription.objects.create(**validated_data)
