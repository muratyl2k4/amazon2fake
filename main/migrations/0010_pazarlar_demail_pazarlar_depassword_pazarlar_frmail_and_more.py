# Generated by Django 4.1.1 on 2023-02-17 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_rename_en_pazarlar_uk"),
    ]

    operations = [
        migrations.AddField(
            model_name="pazarlar",
            name="DEMAIL",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="pazarlar",
            name="DEPASSWORD",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="pazarlar",
            name="FRMAIL",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="pazarlar",
            name="FRPASSWORD",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="pazarlar",
            name="UKMAIL",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="pazarlar",
            name="UKPASSWORD",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]