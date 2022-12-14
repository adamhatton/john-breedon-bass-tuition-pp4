# Generated by Django 3.2.14 on 2022-08-22 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0006_rename_learner_booking_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="type",
            field=models.CharField(
                choices=[
                    ("", "Pick a lesson type"),
                    ("H", "Home visit"),
                    ("O", "Online"),
                    ("S", "At the Studio"),
                ],
                help_text="Please note that I only do home visits in Newcastle",
                max_length=1,
            ),
        ),
    ]
