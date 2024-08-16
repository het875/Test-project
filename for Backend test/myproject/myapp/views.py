from django.shortcuts import render

from pyexpat.errors import messages

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from django.http import HttpResponseBadRequest, HttpResponse 
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from django.shortcuts import render ,get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import qrcode
from io import BytesIO
from .models import QRCodeData
from .serializers import QRCodeDataSerializer
from django.core.files.base import ContentFile
import random
import string  # for generating random strings

# @api_view(['POST'])
# def generate_and_save_qr(request):
#     data = request.data.get('data', '')

#     # Generate a random 6-digit number
#     random_number = ''.join(random.choices(string.digits, k=6))

#     # Generate QR code image
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")

#     # Save QR code image to in-memory file
#     buffer = BytesIO()
#     img.save(buffer, format='PNG')
#     image_file = ContentFile(buffer.getvalue())

#     # Save QR code data to database
#     qr_code_data = QRCodeData(data=data, qr_code_number=random_number)
#     qr_code_data.qr_code.save(f'{data}.png', image_file)
#     qr_code_data.save()

#     # Serialize QR code data for response
#     serializer = QRCodeDataSerializer(qr_code_data)
    
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.utils.encoding import escape_uri_path

# @api_view(['POST'])
# def generate_and_save_qr(request):
#     data = request.data.get('data', '')

#     # Generate a random 6-digit number
#     random_number = ''.join(random.choices(string.digits, k=6))

#     # Generate QR code image
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")

#     # Save QR code image to in-memory file
#     buffer = BytesIO()
#     img.save(buffer, format='PNG')
#     image_file = ContentFile(buffer.getvalue())

#     # Save QR code data to database
#     qr_code_data = QRCodeData(data=data, qr_code_number=random_number)
#     qr_code_data.qr_code.save(f'{data}.png', image_file)
#     qr_code_data.save()

#     # Generate download URL
#     download_url = f"/qr-code/{qr_code_data.id}/download/"

#     # Serialize QR code data for response
#     serializer = QRCodeDataSerializer(qr_code_data)
    
#     # Prepare response JSON
#     response_data = {
#         "qr_code_data": serializer.data,
#         "download_url": download_url,
#     }
    
#     return Response(response_data, status=status.HTTP_201_CREATED)


# # qr_code_api/views.py

# def download_qr_code(request, pk):
#     qr_code_data = get_object_or_404(QRCodeData, pk=pk)
#     image_path = qr_code_data.qr_code.path
#     image_name = qr_code_data.qr_code.name.split('/')[-1]

#     with open(image_path, 'rb') as f:
#         response = HttpResponse(f.read(), content_type='image/png')
#         response['Content-Disposition'] = f'attachment; filename="{escape_uri_path(image_name)}"'
#         return response



# @api_view(['GET'])
# def qr_code_details(request, qr_code_id):
#     try:
#         qr_code_data = QRCodeData.objects.get(pk=qr_code_id)
#     except QRCodeData.DoesNotExist:
#         return Response({'error': 'QR Code not found'}, status=status.HTTP_404_NOT_FOUND)

#     serializer = QRCodeDataSerializer(qr_code_data)
#     return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import QRCodeData
from .serializers import QRCodeDataSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def generate_and_save_qr(request):
    data = request.data.get('data', '')

    # Generate a random 6-digit number
    random_number = ''.join(random.choices(string.digits, k=6))

    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to in-memory file
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_file = ContentFile(buffer.getvalue())

    # Save QR code data to database
    qr_code_data = QRCodeData(original_data=data, qr_code_number=random_number)
    qr_code_data.qr_code.save(f'{data}.png', image_file)

    # Set qr_code_download_url
    qr_code_data.qr_code_download_url = f'http://example.com/media/{qr_code_data.qr_code.name}'  # Replace with your actual domain

    qr_code_data.save()

    # Serialize QR code data for response
    serializer = QRCodeDataSerializer(qr_code_data)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def qr_code_detail(request, pk):
    qr_code_data = get_object_or_404(QRCodeData, pk=pk)
    serializer = QRCodeDataSerializer(qr_code_data)
    return Response(serializer.data)

@api_view(['PUT'])
def qr_code_update(request, pk):
    qr_code_data = get_object_or_404(QRCodeData, pk=pk)
    serializer = QRCodeDataSerializer(qr_code_data, data=request.data)
    if serializer.is_valid():
        # Update qr_code_download_url if qr_code_download changes
        if 'qr_code_download' in request.data:
            qr_code_data.qr_code_download_url = f'http://example.com/media/{qr_code_data.qr_code.name}'  # Replace with your actual domain
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def my_view(request):
    # Process the request data
    message = "Data saved successfully!"
    return Response({"message": message})


