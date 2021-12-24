from rest_framework import serializers
from main.models import Doctor


class DoctorSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=40)
    name = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data):
        return Doctor.objects.create(**validated_data)
