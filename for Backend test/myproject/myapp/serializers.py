from rest_framework import serializers
from .models import *

class QRCodeDataSerializer(serializers.ModelSerializer):
    qr_code_download_url = serializers.SerializerMethodField()

    class Meta:
        model = QRCodeData
        fields = ('id', 'qr_code', 'qr_code_number', 'original_data', 'added_data', 'qr_code_download', 'qr_code_download_url', 'created_at', 'last_modified')
        read_only_fields = ('id', 'qr_code_number', 'created_at', 'last_modified')

    def get_qr_code_download_url(self, obj):
        if obj.qr_code_download:
            return obj.qr_code_download.url
        return None

    def create(self, validated_data):
        qr_code = validated_data.pop('qr_code')
        qr_code_download = validated_data.pop('qr_code_download', None)
        instance = QRCodeData.objects.create(qr_code=qr_code, qr_code_download=qr_code_download, **validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.original_data = validated_data.get('original_data', instance.original_data)
        instance.added_data = validated_data.get('added_data', instance.added_data)
        instance.qr_code_download = validated_data.get('qr_code_download', instance.qr_code_download)
        instance.save()
        return instance
