from django.contrib.auth.models import User
from rest_framework import viewsets

from main.serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = PatientSerializer
