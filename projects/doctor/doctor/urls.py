from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

urlpatterns = [
    path('doctor/', views.DoctorList.as_view()),
    path('doctor/<str:national_id>/', views.DoctorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

