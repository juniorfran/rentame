# Generated by Django 4.2.5 on 2023-11-05 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0013_category_vehicle_category'),
        ('paymentmethod', '0003_banktransferpayment_user_creditcardpayment_user'),
        ('users', '0015_alter_renter_bookings_alter_renter_driving_history_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='bookings',
            field=models.ManyToManyField(blank=True, related_name='renters', to='vehicles.booking'),
        ),
        migrations.AlterField(
            model_name='renter',
            name='preferred_payment_methods',
            field=models.ManyToManyField(related_name='preferred_pago_renters', to='paymentmethod.paymentmethod'),
        ),
    ]