from rest_framework import serializers
from main.models import Patient


class PatientSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=40)
    name = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data):
        return Patient.objects.create(**validated_data)
