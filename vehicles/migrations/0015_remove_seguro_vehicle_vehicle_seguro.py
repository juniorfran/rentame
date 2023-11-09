# Generated by Django 4.2.5 on 2023-11-07 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0014_seguro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seguro',
            name='vehicle',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='seguro',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='seguros', to='vehicles.seguro'),
            preserve_default=False,
        ),
    ]
