# Generated by Django 4.2.5 on 2023-11-17 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_renter_bookings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='apellido',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ciudad',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
