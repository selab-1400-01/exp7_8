from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import generics

from main.serializers import PatientSerializer
from main.models import Patient
from .events import PatientCreationEvent, EventProducer


class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data,
                       status=status.HTTP_201_CREATED, headers=headers)

        if status.is_success(res.status_code):
            producer = EventProducer()
            producer.broadcast_patient_creation(
                PatientCreationEvent(patient, request.data["password"]))

        return res


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'national_id'
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
