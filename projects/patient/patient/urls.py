from django.urls import include, path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('patient/', views.PatientList.as_view()),
    path('patient/<str:national_id>/', views.PatientDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)