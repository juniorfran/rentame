# Generated by Django 4.2.5 on 2023-10-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_vehicleowner_foto2_dui_vehicleowner_foto_licencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='create_add',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='create_add',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='create_add',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicleowner',
            name='create_add',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
