# Generated by Django 5.0.1 on 2024-05-09 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='obras'),
        ),
    ]
