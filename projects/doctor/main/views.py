from rest_framework import status
from rest_framework.response import Response
from main.models import Doctor
from main.serializers import DoctorSerializer
from rest_framework import generics
from .authentication import HasSameNationalIdPermission
from .events import DoctorCreationEvent, EventProducer


class DoctorList(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data,
                       status=status.HTTP_201_CREATED, headers=headers)

        if status.is_success(res.status_code):
            producer = EventProducer()
            producer.broadcast_doctor_creation(
                DoctorCreationEvent(doctor, request.data["password"]))

        return res


class DoctorDetail(generics.RetrieveAPIView):
    lookup_field = 'national_id'
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [HasSameNationalIdPermission]
