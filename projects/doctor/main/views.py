from main.models import Doctor
from main.serializers import DoctorSerializer
from rest_framework import generics


class DoctorList(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'national_id'
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
