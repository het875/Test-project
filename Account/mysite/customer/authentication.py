from rest_framework_simplejwt.authentication import JWTAuthentication
from .tokens import CustomRefreshToken

class CustomJWTAuthentication(JWTAuthentication):
    def get_refresh_token(self, user):
        return CustomRefreshToken.for_user(user)
