# Generated by Django 4.1.7 on 2023-06-10 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("remote", "0005_alter_completedau_asin_alter_completedau_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="completedau",
            name="Date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="completedca",
            name="Date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="completedde",
            name="Date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="completedfr",
            name="Date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="completedja",
            name="Date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="completeduk",
            name="Date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
