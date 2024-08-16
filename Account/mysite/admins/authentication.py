from rest_framework_simplejwt.authentication import JWTAuthentication
from .tokens import AdminsRefreshToken

class CustomJWTAuthentication(JWTAuthentication):
    def get_refresh_token(self, user):
        return AdminsRefreshToken.for_user(user)
