# Generated by Django 3.2.14 on 2022-08-19 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_booking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.CharField(choices=[('', 'Pick a time slot'), ('10', '10:00 - 11:00'), ('11', '11:00 - 12:00'), ('13', '13:00 - 14:00'), ('14', '14:00 - 15:00'), ('15', '15:00 - 16:00'), ('16', '16:00 - 17:00')], max_length=2),
        ),
        migrations.AlterField(
            model_name='booking',
            name='type',
            field=models.CharField(blank=True, choices=[('', 'Pick a date'), ('H', 'Home visit'), ('O', 'Online'), ('S', 'At the Studio')], max_length=1),
        ),
    ]
