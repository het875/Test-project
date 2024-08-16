from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AdminRegisterSerializer, AdminLoginSerializer
from .tokens import AdminsRefreshToken
from django.views.decorators.csrf import csrf_exempt


class AdminRegisterView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            return Response({
                "status": "success",
                "message": "Admin registered successfully.",
                "data": AdminRegisterSerializer(admin).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Registration failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AdminLoginView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.validated_data['admin']
            refresh = AdminsRefreshToken.for_user(admin)
            return Response({
                "status": "success",
                "message": "Login successful.",
                "data": {
                    "admin_id": admin.admin_id,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            })
        return Response({
            "status": "error",
            "message": "Invalid credentials."
        }, status=status.HTTP_401_UNAUTHORIZED)

class AdminLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"status": "error", "message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = AdminsRefreshToken(refresh_token)
                token.blacklist()  # Adjust if using a different blacklisting method
            except Exception as e:
                return Response({"status": "error", "message": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "success", "message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)