from main.models import Patient
from main.serializers import PatientSerializer
from rest_framework import generics


class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer



class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'national_id'
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
