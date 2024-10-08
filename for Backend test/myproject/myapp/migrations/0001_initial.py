# Generated by Django 5.0.7 on 2024-08-01 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="QRCodeData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("qr_code", models.ImageField(upload_to="qr_codes/")),
                ("qr_code_number", models.CharField(max_length=6)),
                ("data", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="QRCodeAdditionalData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("additional_data", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "qr_code_data",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="additional_data",
                        to="myapp.qrcodedata",
                    ),
                ),
            ],
        ),
    ]
