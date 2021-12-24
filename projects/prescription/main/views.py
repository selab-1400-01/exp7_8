from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from main.models import Prescription
from main.serializers import PrescriptionSerializer
from rest_framework import generics
from rest_framework.views import APIView


class PrescriptionList(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "doctors" in request.user.groups:
            queryset = self.get_queryset().filter(doctor__national_id=request.user.national_id)
        else:
            queryset = self.get_queryset().filter(patient__national_id=request.user.national_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)