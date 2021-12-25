from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json


@swagger_auto_schema(method="POST", request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
@api_view(["GET", "POST"])
def doctor(request: Request):
    url = settings.GATEWAY_ENDPOINTS["doctor"] + "/doctor/"
    return forward_request(request, url)

@swagger_auto_schema(method="POST", request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
@api_view(["GET", "POST"])
def patient(request: Request):
    url = settings.GATEWAY_ENDPOINTS["patient"] + "/patient/"
    return forward_request(request, url)

@swagger_auto_schema(method="POST", request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
@api_view(["POST"])
def prescription_create(request: Request):
    url = settings.GATEWAY_ENDPOINTS["prescription_create"] + "/prescription/"
    return forward_request(request, url)

@swagger_auto_schema(method="GET", request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
@api_view(["GET"])
def prescription_list(request: Request):
    url = settings.GATEWAY_ENDPOINTS["prescription"] + "/prescription/"
    return forward_request(request, url)

@swagger_auto_schema(method="POST", request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
@api_view(["POST"])
def token(request: Request):
    url = settings.GATEWAY_ENDPOINTS["auth"] + "/token/"
    return forward_request(request, url)

@swagger_auto_schema(method="POST", request_body=openapi.Schema(type=openapi.TYPE_OBJECT))
@api_view(["POST"])
def token_refresh(request: Request):
    url = settings.GATEWAY_ENDPOINTS["auth"] + "/token/refresh"
    return forward_request(request, url)




def forward_request(request: Request, url) -> Response:
    result = requests.request(method=request.method, url=url, data=json.dumps(
        request.data), headers=request.headers)
    return HttpResponse(result.content, status=result.status_code, headers=result.headers)
