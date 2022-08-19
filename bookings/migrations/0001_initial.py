# Generated by Django 3.2.14 on 2022-08-19 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Adding a phone number makes it easier for me to contact you about your lesson', max_length=128, region=None)),
                ('type', models.CharField(blank=True, choices=[('H', 'Home visit'), ('O', 'Online'), ('S', 'At the Studio')], max_length=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]