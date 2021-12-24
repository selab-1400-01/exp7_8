from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PatientId
from .authentication import IsDoctorPermission
from .serializers import PrescriptionSerializer
from .events import EventProducer, PrescriptionCreationEvent

from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class PrescriptionCreate(APIView):
    permission_classes = [IsDoctorPermission]

    @swagger_auto_schema(request_body=PrescriptionSerializer)
    def post(self, request, format=None):
        serializer = PrescriptionSerializer(data=request.data)
        if (not serializer.is_valid() or
                not PatientId.objects.exists(
                    national_id=serializer.validated_data.patient_national_id)):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        prescription = serializer.validated_data

        producer = EventProducer()
        producer.broadcast_patient_creation(
            PrescriptionCreationEvent(prescription, request.user.national_id))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
