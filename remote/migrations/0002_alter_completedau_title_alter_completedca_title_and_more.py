# Generated by Django 4.1.7 on 2023-06-07 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("remote", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="completedau",
            name="Title",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="completedca",
            name="Title",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="completedde",
            name="Title",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="completedfr",
            name="Title",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="completedja",
            name="Title",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="completeduk",
            name="Title",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
