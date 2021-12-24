from rest_framework.response import Response

from main.models import Prescription
from main.serializers import PrescriptionSerializer
from rest_framework import generics
from rest_framework.views import APIView


class PrescriptionList(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class PrescriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'patient_national_id'
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def retrieve(self, request, *args, **kwargs):
        pnid = self.kwargs.get('patient_national_id')
        dnid = self.kwargs.get('doctor_national_id')
        object = Prescription.objects.get(patient_national_id=pnid, doctor_national_id=dnid)
        serializer = PrescriptionSerializer(object)
        return Response(serializer.data)
