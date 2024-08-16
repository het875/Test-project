# Generated by Django 5.0.7 on 2024-08-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Admins",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("admin_id", models.AutoField(primary_key=True, serialize=False)),
                ("admin_email", models.EmailField(max_length=55, unique=True)),
                ("username", models.CharField(max_length=55, unique=True)),
                ("password", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
