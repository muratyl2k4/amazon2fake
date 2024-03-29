# Generated by Django 4.1.1 on 2023-02-17 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0007_fransa"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pazarlar",
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
                ("EN", models.BooleanField(blank=True, null=True)),
                ("FR", models.BooleanField(blank=True, null=True)),
                ("DE", models.BooleanField(blank=True, null=True)),
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
        ),
    ]
