import jwt
from inventory_management import settings as settings
from django.http import JsonResponse
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


def custom_response(
    success=False, message="something went wrong", data=None, status=400
):
    response = {"success": success, "message": message, "data": data}
    return JsonResponse(response, status=status)


class CustomAuth(BasePermission):
    def has_permission(self, request, view):
        # Get the Authorization header
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header and auth_header.startswith("Bearer "):
            # Extract the token from the header
            token = auth_header.split()[1]
            try:
                token_data = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                # print(token_data, "()()" * 10)
                request.token_data = token_data

                return True
            except Exception as e:
                raise PermissionDenied("Invalid token")
        else:
            raise PermissionDenied("Missing or invalid Authorization header")


def generate_token(user):
    token = jwt.encode(
        {
            "user_id": str(user.id),
            "role": user.name,
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return token
