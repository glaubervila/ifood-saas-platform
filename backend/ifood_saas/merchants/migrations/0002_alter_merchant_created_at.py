# Generated by Django 5.1.8 on 2025-04-16 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
