# Generated by Django 4.2.5 on 2023-10-25 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0011_alter_vehicle_create_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='climatizacion',
            field=models.CharField(max_length=50, null=True),
        ),
    ]