# Generated by Django 5.1.8 on 2025-04-16 21:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0005_alter_merchantaccess_merchant_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantaccess',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_access', to='merchants.merchant'),
        ),
        migrations.AlterField(
            model_name='merchantaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_access', to=settings.AUTH_USER_MODEL),
        ),
    ]
