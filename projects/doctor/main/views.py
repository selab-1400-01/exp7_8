from django.contrib.auth.models import User
from rest_framework import viewsets

from main.serializers import DoctorSerializer

# class DoctorViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = DoctorSerializer

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
