from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

urlpatterns = [
    path('patient/', views.PatientList.as_view()),
    path('patient/<str:national_id>/', views.PatientDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

