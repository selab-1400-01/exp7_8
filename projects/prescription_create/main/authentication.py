from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.permissions import BasePermission

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            national_id = validated_token["id"]
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')
        
        groups = validated_token.get("groups", list())

        return CustomUser(national_id, groups)

class CustomUser:
    def __init__(self, national_id: str, groups: list) -> None:
        self.national_id = national_id
        self.groups = groups

class IsDoctorPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user:
            return False
        
        if not (hasattr(request.user, "national_id") and hasattr(request.user, "groups")):
            return False

        return "doctors" in request.user.groups