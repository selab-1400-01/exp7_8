from rest_framework import serializers

class PrescriptionSerializer(serializers.Serializer):
    patient_national_id = serializers.CharField(max_length=40)
    drugs_list = serializers.CharField(max_length=255, default="")
    comment = serializers.CharField(max_length=255, allow_blank=True, default="")
