# Generated by Django 3.2.14 on 2022-08-11 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_auto_20220730_1259"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contact",
            options={"ordering": ["-submitted"]},
        ),
    ]
