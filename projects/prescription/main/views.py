from main.models import Prescription
from main.serializers import PrescriptionSerializer
from rest_framework import generics


class PrescriptionList(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class PrescriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'national_id'
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
