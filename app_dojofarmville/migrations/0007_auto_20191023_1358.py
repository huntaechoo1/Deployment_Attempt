# Generated by Django 2.2.6 on 2019-10-23 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_dojofarmville', '0006_auto_20191023_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='farm', to='app_dojofarmville.User'),
        ),
    ]
