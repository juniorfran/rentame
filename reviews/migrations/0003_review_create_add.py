# Generated by Django 4.2.5 on 2023-10-15 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='create_add',
            field=models.DateField(null=True),
        ),
    ]
