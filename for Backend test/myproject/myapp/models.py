from django.db import models

class QRCodeData(models.Model):
    qr_code = models.ImageField(upload_to='qr_codes/')
    qr_code_number = models.CharField(max_length=6)
    original_data = models.TextField()
    added_data = models.TextField(blank=True)
    qr_code_download = models.ImageField(upload_to='qr_code_downloads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    qr_code_download_url = models.URLField(blank=True)

    def __str__(self):
        return f'QR Code for {self.original_data}'
