from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer, LoginSerializer
from .models import Customer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({
                "status": "success",
                "message": "User registered successfully.",
                "data": RegisterSerializer(customer).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Registration failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
from .tokens import CustomRefreshToken

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.validated_data['customer']
            refresh = CustomRefreshToken.for_user(customer)  # Use the custom token class
            return Response({
                "status": "success",
                "message": "Login successful.",
                "data": {
                    "cust_id": customer.cust_id,  # Include cust_id in the response
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            })
        return Response({
            "status": "error",
            "message": "Invalid credentials."
        }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "status": "success",
                "message": "Logout successful."
            }, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response({
                "status": "error",
                "message": "Invalid or expired token.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
