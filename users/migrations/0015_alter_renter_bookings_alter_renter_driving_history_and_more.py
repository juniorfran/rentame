# Generated by Django 4.2.5 on 2023-11-05 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentmethod', '0003_banktransferpayment_user_creditcardpayment_user'),
        ('vehicles', '0013_category_vehicle_category'),
        ('users', '0014_userprofile_fecha_nacimeinto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='bookings',
            field=models.ManyToManyField(blank=True, null=True, related_name='renters', to='vehicles.booking'),
        ),
        migrations.AlterField(
            model_name='renter',
            name='driving_history',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='renter',
            name='preferred_payment_methods',
            field=models.ManyToManyField(null=True, related_name='preferred_pago_renters', to='paymentmethod.paymentmethod'),
        ),
        migrations.AlterField(
            model_name='renter',
            name='required_documents',
            field=models.CharField(max_length=100),
        ),
    ]
