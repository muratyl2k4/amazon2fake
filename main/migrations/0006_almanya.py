# Generated by Django 4.1.1 on 2023-02-14 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0005_rename_data_ingiltere"),
    ]

    operations = [
        migrations.CreateModel(
            name="Almanya",
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
                (
                    "uuid",
                    models.UUIDField(
                        blank=True, editable=False, null=True, unique=True
                    ),
                ),
                ("TARIH", models.DateField(blank=True, null=True)),
                ("ASIN", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "ALICI_SIPARIS_NUMARASI",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "SATICI_SIPARIS_NUMARASI",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("SATIS_FIYATI", models.FloatField(blank=True, null=True)),
                ("AMAZON_FEE", models.FloatField(blank=True, null=True)),
                ("MALIYET", models.FloatField(blank=True, null=True)),
                ("DEPO_MALIYET", models.FloatField(blank=True, null=True)),
                ("KAR", models.FloatField(blank=True, null=True)),
                ("YUZDELIK_KAR", models.FloatField(blank=True, null=True)),
                (
                    "KULLANICI",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
